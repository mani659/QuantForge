import pyarrow as pa
import pyarrow.parquet as pq
import struct
import hashlib
from pathlib import Path
import json

class TickParquetConverter:
    SCHEMA = pa.schema([
        ("source_row_ordinal", pa.int64()),
        ("date", pa.string()),
        ("time", pa.string()),
        ("bid", pa.float64()),
        ("ask", pa.float64()),
        ("last", pa.float64()),
        ("vol", pa.float64())
    ])

    def __init__(self, output_dir: Path, market: str, chunk_size: int = 100000, compression: str = "snappy"):
        self.output_dir = Path(output_dir)
        self.market = market
        self.chunk_size = chunk_size
        self.compression = compression
        
        self.current_partition = None
        self.writer = None
        self.rows_buffer = {
            "source_row_ordinal": [],
            "date": [],
            "time": [],
            "bid": [],
            "ask": [],
            "last": [],
            "vol": []
        }
        self.buffer_count = 0
        self.total_rows = 0
        self.partition_inventory = []
        
        # 7 Hashers
        self.hashers = {
            "source_row_ordinal": hashlib.sha256(),
            "date": hashlib.sha256(),
            "time": hashlib.sha256(),
            "bid": hashlib.sha256(),
            "ask": hashlib.sha256(),
            "last": hashlib.sha256(),
            "vol": hashlib.sha256()
        }

    def _flush_buffer(self):
        if self.buffer_count == 0:
            return
        table = pa.Table.from_pydict(self.rows_buffer, schema=self.SCHEMA)
        self.writer.write_table(table)
        
        for k in self.rows_buffer:
            self.rows_buffer[k].clear()
        self.buffer_count = 0

    def _close_writer(self):
        self._flush_buffer()
        if self.writer:
            self.writer.close()
            self.writer = None

    def _get_partition_path(self, yyyymm: str) -> Path:
        partition_dir = self.output_dir / self.market
        partition_dir.mkdir(parents=True, exist_ok=True)
        return partition_dir / f"{yyyymm}.parquet"

    def process_file(self, input_csv: Path, production_mode: bool = False, expected_source_sha: str = None, expected_converter_sha: str = None, expected_spec_sha: str = None):
        input_csv = Path(input_csv).resolve()
        
        # PRODUCTION FIREWALL
        if "data" in input_csv.parts or "production" in input_csv.name.lower():
            if not production_mode:
                raise RuntimeError("EXECUTION-INFRASTRUCTURE FAILURE: Production data access forbidden.")
                
            if input_csv.name != "XAGUSD_mt5_ticks.csv":
                raise RuntimeError("EXECUTION-INFRASTRUCTURE FAILURE: Only XAGUSD_mt5_ticks.csv is registered for production conversion.")
                
            if expected_source_sha != "edccad88ed5b74caf16a14203f3cf743306c65f2ebc5004cf566ed61deeb6e17":
                raise RuntimeError("EXECUTION-INFRASTRUCTURE FAILURE: Provided source SHA does not match registered production SHA.")
                
            if expected_spec_sha != "b71ca7689acb06f949b5457cfcb9ed4a20ebaaa80662e9c62138df02fcb4b630" or self.get_spec_hash() != expected_spec_sha:
                raise RuntimeError("EXECUTION-INFRASTRUCTURE FAILURE: Specification identity mismatch.")
                
            if self.get_implementation_hash() != expected_converter_sha:
                raise RuntimeError("EXECUTION-INFRASTRUCTURE FAILURE: Converter identity mismatch.")
                
            if (self.output_dir / self.market).exists() and list((self.output_dir / self.market).glob("*.parquet")):
                raise RuntimeError("EXECUTION-INFRASTRUCTURE FAILURE: Output directory already contains parquet files. Overwrite refused.")

        hasher_csv = hashlib.sha256()
        
        try:
            with open(input_csv, 'rb') as f:
                for line_bytes in f:
                    hasher_csv.update(line_bytes)
                    line = line_bytes.decode('utf-8').strip()
                    if not line:
                        continue
                    parts = line.split(',')
                    if len(parts) != 6:
                        raise RuntimeError(f"EXECUTION-INFRASTRUCTURE FAILURE: Invalid column count. {line}")
                    
                    date_str = parts[0]
                    time_str = parts[1]
                    bid_str = parts[2]
                    ask_str = parts[3]
                    last_str = parts[4]
                    vol_str = parts[5]
                    
                    try:
                        bid_val = float(bid_str)
                        ask_val = float(ask_str)
                        vol_val = float(vol_str)
                        if last_str == "":
                            last_val = None
                        else:
                            last_val = float(last_str)
                    except ValueError as e:
                        raise RuntimeError(f"EXECUTION-INFRASTRUCTURE FAILURE: Float parsing error. {e}")

                    yyyymm = date_str[:6]
                    if len(yyyymm) != 6 or not yyyymm.isdigit():
                        raise RuntimeError("EXECUTION-INFRASTRUCTURE FAILURE: Invalid date format.")
                        
                    if self.current_partition != yyyymm:
                        if self.current_partition is not None and int(yyyymm) < int(self.current_partition):
                            raise RuntimeError("EXECUTION-INFRASTRUCTURE FAILURE: Non-chronological partition encountered.")
                        self._close_writer()
                        self.current_partition = yyyymm
                        part_path = self._get_partition_path(yyyymm)
                        self.writer = pq.ParquetWriter(part_path, self.SCHEMA, compression=self.compression)
                        if str(part_path) not in self.partition_inventory:
                            self.partition_inventory.append(str(part_path))
                    
                    ordinal = self.total_rows
                    self.rows_buffer["source_row_ordinal"].append(ordinal)
                    self.rows_buffer["date"].append(date_str)
                    self.rows_buffer["time"].append(time_str)
                    self.rows_buffer["bid"].append(bid_val)
                    self.rows_buffer["ask"].append(ask_val)
                    self.rows_buffer["last"].append(last_val)
                    self.rows_buffer["vol"].append(vol_val)
                    
                    self.hashers["source_row_ordinal"].update(struct.pack('<q', ordinal))
                    
                    date_encoded = date_str.encode('utf-8')
                    self.hashers["date"].update(struct.pack('<I', len(date_encoded)) + date_encoded)
                    
                    time_encoded = time_str.encode('utf-8')
                    self.hashers["time"].update(struct.pack('<I', len(time_encoded)) + time_encoded)
                    
                    self.hashers["bid"].update(struct.pack('<d', bid_val))
                    self.hashers["ask"].update(struct.pack('<d', ask_val))
                    
                    if last_val is None:
                        self.hashers["last"].update(b'\x00')
                    else:
                        self.hashers["last"].update(b'\x01' + struct.pack('<d', last_val))
                        
                    self.hashers["vol"].update(struct.pack('<d', vol_val))
                    
                    self.total_rows += 1
                    self.buffer_count += 1
                    
                    if self.buffer_count >= self.chunk_size:
                        self._flush_buffer()
                        
            self._close_writer()
            
            final_csv_sha = hasher_csv.hexdigest()
            if production_mode and final_csv_sha != expected_source_sha:
                raise RuntimeError("EXECUTION-INFRASTRUCTURE FAILURE: Processed CSV SHA-256 does not match registered expected SHA-256.")
            
            manifest = {
                "source_csv_sha256": final_csv_sha,
                "converter_implementation_sha256": self.get_implementation_hash(),
                "specification_sha256": self.get_spec_hash(),
                "schema_version": "V2",
                "row_count": self.total_rows,
                "partitions": [Path(p).name for p in self.partition_inventory], # Keep relative names for canonical check
                "column_hashes": {k: v.hexdigest() for k, v in self.hashers.items()}
            }
            
            with open(self.output_dir / "manifest.json", "w") as f:
                json.dump(manifest, f, indent=2)
                
            return manifest
            
        except Exception as e:
            self._close_writer()
            if "EXECUTION-INFRASTRUCTURE FAILURE" not in str(e):
                raise RuntimeError(f"EXECUTION-INFRASTRUCTURE FAILURE: {e}") from e
            raise

    def get_implementation_hash(self):
        with open(__file__, 'rb') as f:
            return hashlib.sha256(f.read()).hexdigest()
            
    def get_spec_hash(self):
        spec_path = Path(__file__).parent.parent.parent / "output" / "research_discovery" / "ORD_TICK_PARQUET_CONVERSION_SPECIFICATION_V2.md"
        if spec_path.exists():
            with open(spec_path, 'rb') as f:
                return hashlib.sha256(f.read()).hexdigest()
        return "SPEC_NOT_FOUND_OR_SYNTHETIC"

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Tick Parquet Converter")
    parser.add_argument("input_csv", help="Path to input CSV")
    parser.add_argument("output_dir", help="Path to output directory")
    parser.add_argument("market", help="Market name")
    parser.add_argument("--test", action="store_true", help="Synthetic test mode (default)")
    parser.add_argument("--production", action="store_true", help="Authorize production conversion")
    parser.add_argument("--expected-source-sha", type=str, help="Expected source CSV SHA-256 (required for production)")
    parser.add_argument("--expected-converter-sha", type=str, help="Expected converter script SHA-256 (required for production)")
    parser.add_argument("--expected-spec-sha", type=str, help="Expected specification SHA-256 (required for production)")
    
    args = parser.parse_args()
    
    converter = TickParquetConverter(args.output_dir, args.market)
    manifest = converter.process_file(
        args.input_csv,
        production_mode=args.production,
        expected_source_sha=args.expected_source_sha,
        expected_converter_sha=args.expected_converter_sha,
        expected_spec_sha=args.expected_spec_sha
    )
    print("Conversion complete.")
    print(json.dumps(manifest, indent=2))
