class EventStateMachine:
    def __init__(self):
        self.state = "IDLE"
        self.current_event = None
        self.transitions = []
        
    def _transition(self, new_state, timestamp, metadata=None):
        old_state = self.state
        self.state = new_state
        self.transitions.append({
            "timestamp": timestamp,
            "old_state": old_state,
            "new_state": new_state,
            "metadata": metadata
        })
        
    def handle_signal(self, signal, timestamp):
        if self.state == "IDLE":
            self.current_event = signal
            self._transition("EVENT_DETECTED", timestamp, {"signal": signal})
            self._transition("ENTRY_PENDING", timestamp)
            return True
        else:
            # We enforce that a single shock must not create multiple opportunities
            # Actually, signal_engine lockout handles duplicate shocks, but if one occurs while not IDLE, we drop it.
            return False
            
    def handle_entry(self, execution_report, timestamp):
        if self.state == "ENTRY_PENDING":
            self._transition("OBSERVED_ENTRY", timestamp, execution_report)
            self._transition("IN_POSITION", timestamp)
            return True
        return False
        
    def trigger_exit(self, timestamp):
        if self.state == "IN_POSITION":
            self._transition("EXIT_PENDING", timestamp)
            return True
        return False
        
    def handle_exit(self, execution_report, timestamp):
        if self.state == "EXIT_PENDING":
            self._transition("OBSERVED_EXIT", timestamp, execution_report)
            self._transition("CLOSED", timestamp)
            # Reset state for next event
            self.state = "IDLE"
            self.current_event = None
            return True
        return False
