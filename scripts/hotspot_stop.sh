#!/bin/bash

echo "❄️  Stopping Hotspot..."

# Kill services
killall hostapd 2>/dev/null || true
killall dnsmasq 2>/dev/null || true

# Restore Interface (Optional: could restart wpa_supplicant if we want to reconnect to home wifi)
ifconfig wlan0 down
ifconfig wlan0 up

# Flush IPtables (Basic cleanup)
iptables -F
iptables -t nat -F

echo "✅ Hotspot stopped."
