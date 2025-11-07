# sms_api.py - SMS and WhatsApp notification system
import requests
import logging
from datetime import datetime
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NotificationAPI:
    def __init__(self, twilio_sid=None, twilio_token=None, whatsapp_token=None):
        self.twilio_sid = twilio_sid or "demo_sid"
        self.twilio_token = twilio_token or "demo_token"
        self.whatsapp_token = whatsapp_token or "demo_token"
        self.twilio_url = "https://api.twilio.com/2010-04-01/Accounts"
    
    def send_sms(self, phone_number, message):
        """Send SMS using Twilio API"""
        try:
            if self.twilio_sid == "demo_sid":
                return self.send_mock_sms(phone_number, message)
            
            # Real Twilio SMS (when credentials are available)
            url = f"{self.twilio_url}/{self.twilio_sid}/Messages.json"
            
            data = {
                'From': '+1234567890',  # Your Twilio phone number
                'To': phone_number,
                'Body': message
            }
            
            response = requests.post(url, data=data, auth=(self.twilio_sid, self.twilio_token))
            response.raise_for_status()
            
            result = response.json()
            logger.info(f"SMS sent successfully to {phone_number}")
            
            return {
                'status': 'success',
                'message_id': result['sid'],
                'phone': phone_number,
                'message': message,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error sending SMS: {str(e)}")
            return {
                'status': 'error',
                'error': str(e),
                'phone': phone_number,
                'message': message,
                'timestamp': datetime.now().isoformat()
            }
    
    def send_whatsapp(self, phone_number, message):
        """Send WhatsApp message using WhatsApp Business API"""
        try:
            if self.whatsapp_token == "demo_token":
                return self.send_mock_whatsapp(phone_number, message)
            
            # Real WhatsApp API call (when token is available)
            url = "https://graph.facebook.com/v17.0/YOUR_PHONE_NUMBER_ID/messages"
            
            headers = {
                'Authorization': f'Bearer {self.whatsapp_token}',
                'Content-Type': 'application/json'
            }
            
            data = {
                'messaging_product': 'whatsapp',
                'to': phone_number,
                'type': 'text',
                'text': {'body': message}
            }
            
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            
            result = response.json()
            logger.info(f"WhatsApp message sent successfully to {phone_number}")
            
            return {
                'status': 'success',
                'message_id': result['messages'][0]['id'],
                'phone': phone_number,
                'message': message,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error sending WhatsApp: {str(e)}")
            return {
                'status': 'error',
                'error': str(e),
                'phone': phone_number,
                'message': message,
                'timestamp': datetime.now().isoformat()
            }
    
    def send_mock_sms(self, phone_number, message):
        """Mock SMS sending for demo purposes"""
        logger.info(f"[MOCK SMS] To: {phone_number}")
        logger.info(f"[MOCK SMS] Message: {message}")
        
        return {
            'status': 'success',
            'message_id': f'mock_sms_{datetime.now().strftime("%Y%m%d%H%M%S")}',
            'phone': phone_number,
            'message': message,
            'timestamp': datetime.now().isoformat(),
            'method': 'mock'
        }
    
    def send_mock_whatsapp(self, phone_number, message):
        """Mock WhatsApp sending for demo purposes"""
        logger.info(f"[MOCK WHATSAPP] To: {phone_number}")
        logger.info(f"[MOCK WHATSAPP] Message: {message}")
        
        return {
            'status': 'success',
            'message_id': f'mock_wa_{datetime.now().strftime("%Y%m%d%H%M%S")}',
            'phone': phone_number,
            'message': message,
            'timestamp': datetime.now().isoformat(),
            'method': 'mock'
        }
    
    def send_weather_alert(self, phone_number, district, alert_data):
        """Send formatted weather alert"""
        try:
            message = f"🌦️ Weather Alert for {district}\n\n"
            message += f"📍 District: {district}\n"
            message += f"🌡️ Temperature: {alert_data.get('temperature', 'N/A')}°C\n"
            message += f"💧 Humidity: {alert_data.get('humidity', 'N/A')}%\n\n"
            
            if alert_data.get('alerts'):
                message += "⚠️ Alerts:\n"
                for alert in alert_data['alerts']:
                    message += f"• {alert['message']}\n"
                    if alert.get('recommendation'):
                        message += f"  💡 {alert['recommendation']}\n"
            
            message += f"\n🕒 Time: {datetime.now().strftime('%d-%m-%Y %H:%M')}\n"
            message += "📱 SmartCrop Advisory System"
            
            # Send both SMS and WhatsApp
            sms_result = self.send_sms(phone_number, message)
            whatsapp_result = self.send_whatsapp(phone_number, message)
            
            return {
                'sms': sms_result,
                'whatsapp': whatsapp_result,
                'phone': phone_number,
                'district': district,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error sending weather alert: {str(e)}")
            return {
                'status': 'error',
                'error': str(e),
                'phone': phone_number,
                'district': district,
                'timestamp': datetime.now().isoformat()
            }
    
    def send_crop_alert(self, phone_number, district, crop_data):
        """Send crop-specific alerts"""
        try:
            message = f"🌱 Crop Alert for {district}\n\n"
            message += f"📍 District: {district}\n"
            message += f"🌾 Recommended Crop: {crop_data.get('crop', 'N/A')}\n"
            message += f"📊 Confidence: {crop_data.get('confidence', 0)*100:.1f}%\n\n"
            
            if crop_data.get('fertilizer_gap'):
                message += "💊 Fertilizer Recommendations:\n"
                gap = crop_data['fertilizer_gap']
                if gap.get('nitrogen_gap', 0) > 0:
                    message += f"• Nitrogen: {gap['nitrogen_gap']:.1f} kg/ha\n"
                if gap.get('phosphorus_gap', 0) > 0:
                    message += f"• Phosphorus: {gap['phosphorus_gap']:.1f} kg/ha\n"
                if gap.get('potassium_gap', 0) > 0:
                    message += f"• Potassium: {gap['potassium_gap']:.1f} kg/ha\n"
            
            message += f"\n🕒 Time: {datetime.now().strftime('%d-%m-%Y %H:%M')}\n"
            message += "📱 SmartCrop Advisory System"
            
            # Send both SMS and WhatsApp
            sms_result = self.send_sms(phone_number, message)
            whatsapp_result = self.send_whatsapp(phone_number, message)
            
            return {
                'sms': sms_result,
                'whatsapp': whatsapp_result,
                'phone': phone_number,
                'district': district,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error sending crop alert: {str(e)}")
            return {
                'status': 'error',
                'error': str(e),
                'phone': phone_number,
                'district': district,
                'timestamp': datetime.now().isoformat()
            }

# Global notification API instance
notification_api = NotificationAPI()

def send_weather_alert_to_farmer(phone_number, district, alert_data):
    """Public interface for sending weather alerts"""
    return notification_api.send_weather_alert(phone_number, district, alert_data)

def send_crop_alert_to_farmer(phone_number, district, crop_data):
    """Public interface for sending crop alerts"""
    return notification_api.send_crop_alert(phone_number, district, crop_data)

def send_sms_to_farmer(phone_number, message):
    """Public interface for sending SMS"""
    return notification_api.send_sms(phone_number, message)

def send_whatsapp_to_farmer(phone_number, message):
    """Public interface for sending WhatsApp"""
    return notification_api.send_whatsapp(phone_number, message)
