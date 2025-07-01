#!/usr/bin/env python3
"""
IoT Device Simulator
Simulates multiple IoT devices sending heartbeats to the monitoring system.
"""

import asyncio
import aiohttp
import random
import time
import json
from datetime import datetime
from typing import Dict, List

class IoTDeviceSimulator:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.devices = [
            {
                "device_id": "sensor-001",
                "name": "Temperature Sensor - Living Room",
                "location": "Living Room",
                "battery_level": 85.0,
                "signal_strength": -45.0
            },
            {
                "device_id": "sensor-002", 
                "name": "Humidity Sensor - Kitchen",
                "location": "Kitchen",
                "battery_level": 92.0,
                "signal_strength": -52.0
            },
            {
                "device_id": "sensor-003",
                "name": "Motion Sensor - Front Door",
                "location": "Front Door",
                "battery_level": 78.0,
                "signal_strength": -48.0
            },
            {
                "device_id": "sensor-004",
                "name": "Light Sensor - Bedroom",
                "location": "Bedroom",
                "battery_level": 45.0,  # Low battery to test at-risk status
                "signal_strength": -55.0
            },
            {
                "device_id": "sensor-005",
                "name": "Security Camera - Backyard",
                "location": "Backyard",
                "battery_level": 15.0,  # Very low battery
                "signal_strength": -60.0
            }
        ]
        
    async def send_heartbeat(self, session: aiohttp.ClientSession, device: Dict) -> None:
        """Send a heartbeat for a specific device"""
        try:
            # Simulate some realistic variations
            battery_variation = random.uniform(-2.0, 1.0)
            signal_variation = random.uniform(-3.0, 2.0)
            
            heartbeat_data = {
                "device_id": device["device_id"],
                "name": device["name"],
                "battery_level": max(0.0, min(100.0, device["battery_level"] + battery_variation)),
                "signal_strength": device["signal_strength"] + signal_variation,
                "location": device["location"]
            }
            
            # Update device state for next iteration
            device["battery_level"] = heartbeat_data["battery_level"]
            device["signal_strength"] = heartbeat_data["signal_strength"]
            
            async with session.post(
                f"{self.base_url}/heartbeat",
                json=heartbeat_data,
                headers={"Content-Type": "application/json"}
            ) as response:
                if response.status == 200:
                    result = await response.json()
                    print(f"✅ {device['name']} heartbeat sent - Status: {result.get('status', 'unknown')}")
                else:
                    print(f"❌ Failed to send heartbeat for {device['name']}: {response.status}")
                    
        except Exception as e:
            print(f"❌ Error sending heartbeat for {device['name']}: {e}")
    
    async def simulate_device_behavior(self, session: aiohttp.ClientSession, device: Dict) -> None:
        """Simulate realistic device behavior with varying intervals"""
        while True:
            # Random interval between 30-90 seconds
            interval = random.uniform(30, 90)
            
            # Simulate occasional device failures (5% chance)
            if random.random() < 0.05:
                print(f"⚠️  {device['name']} temporarily offline (simulated failure)")
                await asyncio.sleep(interval * 2)  # Longer sleep for "failed" devices
                continue
            
            await self.send_heartbeat(session, device)
            await asyncio.sleep(interval)
    
    async def run_simulation(self, duration_minutes: int = 10) -> None:
        """Run the device simulation for a specified duration"""
        print(f"🚀 Starting IoT device simulation for {duration_minutes} minutes...")
        print(f"📡 Simulating {len(self.devices)} devices")
        print(f"🌐 Target URL: {self.base_url}")
        print("-" * 50)
        
        async with aiohttp.ClientSession() as session:
            # Start all device simulations
            tasks = [
                self.simulate_device_behavior(session, device)
                for device in self.devices
            ]
            
            # Run for specified duration
            try:
                await asyncio.wait_for(
                    asyncio.gather(*tasks),
                    timeout=duration_minutes * 60
                )
            except asyncio.TimeoutError:
                print(f"\n⏰ Simulation completed after {duration_minutes} minutes")
            
            print("🏁 Simulation finished!")

async def main():
    """Main function to run the simulation"""
    import argparse
    
    parser = argparse.ArgumentParser(description="IoT Device Heartbeat Simulator")
    parser.add_argument(
        "--url", 
        default="http://localhost:8000",
        help="Base URL of the IoT monitoring service"
    )
    parser.add_argument(
        "--duration", 
        type=int, 
        default=10,
        help="Simulation duration in minutes"
    )
    
    args = parser.parse_args()
    
    simulator = IoTDeviceSimulator(args.url)
    await simulator.run_simulation(args.duration)

if __name__ == "__main__":
    asyncio.run(main()) 