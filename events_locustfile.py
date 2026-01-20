from locust import HttpUser, task, between, constant_throughput
import random

class EventsUser(HttpUser):
    wait_time = constant_throughput(1.0)  # 1 request per second
    
    def on_start(self):
        """Called when a locust user starts"""
        self.user_id = random.randint(1, 100)

    @task(3)
    def view_events(self):
        """View events with user parameter"""
        response = self.client.get(
            "/events",
            params={"user": f"locust_user_{self.user_id}"},
            name="/events"
        )
        response.raise_for_status()

    @task(1)
    def view_events_filtered(self):
        """View events with different filters"""
        response = self.client.get(
            "/events",
            params={"user": f"locust_user_{self.user_id}", "limit": 10},
            name="/events?limit=10"
        )
        response.raise_for_status()
