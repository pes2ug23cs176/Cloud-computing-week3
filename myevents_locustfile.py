from locust import HttpUser, task, between, constant_throughput
import random
import time

class MyEventsUser(HttpUser):
    wait_time = constant_throughput(1.0)  # 1 request per second
    
    def on_start(self):
        """Called when a locust user starts"""
        self.user_id = random.randint(1, 100)
        self.start_time = time.time()

    @task(2)
    def view_my_events(self):
        """View user's own events"""
        response = self.client.get(
            "/my-events",
            params={"user": f"locust_user_{self.user_id}"},
            name="/my-events"
        )
        response.raise_for_status()

    @task(1)
    def view_my_events_sorted(self):
        """View user's events with sorting"""
        response = self.client.get(
            "/my-events",
            params={"user": f"locust_user_{self.user_id}", "sort": "date"},
            name="/my-events?sort=date"
        )
        response.raise_for_status()

    @task(1)
    def view_my_events_paginated(self):
        """View user's events with pagination"""
        response = self.client.get(
            "/my-events",
            params={"user": f"locust_user_{self.user_id}", "limit": 5, "offset": 0},
            name="/my-events?limit=5"
        )
        response.raise_for_status()
