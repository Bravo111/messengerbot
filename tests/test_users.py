from unittest import TestCase
from messengerbot import MessengerClient, messages, MessengerException, users
from mock import patch


class UserTestCase(TestCase):

    @patch('requests.get')
    def test_get_user_profile(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
          "first_name": "Peter",
          "last_name": "Chang",
          "profile_pic": "https://fbcdn-profile-a.akamaihd.net/hprofile-ak-xpf1/v/t1.0-1/p200x200/13055603_10105219398495383_8237637584159975445_n.jpg?oh=1d241d4b6d4dac50eaf9bb73288ea192&oe=57AF5C03&__gda__=1470213755_ab17c8c8e3a0a447fed3f272fa2179ce",
          "locale": "en_US",
          "timezone": -7,
          "gender": "male"
        }
        recipient = messages.Recipient(recipient_id='123')
        messenger_user_profile = users.MessengerUserProfile(access_token='1234',
                                                      recipient=recipient)
        result = messenger_user_profile.get_user_profile()

        mock_get.assert_called_with(
            'https://graph.facebook.com/v2.6/123',
            params={'access_token': '1234',
                    'fields' : 'first_name,last_name,profile_pic,locale,timezone,gender' }
        )

    @patch('requests.get')
    def test_client_send_error_with_error_data(self, mock_get):
        mock_get.return_value.status_code = 190
        mock_get.return_value.json.return_value = {
            "error":{
                     "message":"Invalid parameter",
                     "type":"FacebookApiException",
                     "code":100,
                     "error_data":"No matching user found.",
                     "fbtrace_id":"D2kxCybrKVw"
                     }
        }

        recipient = messages.Recipient(recipient_id='123')
        messenger_user_profile = users.MessengerUserProfile(access_token='1234',
                                                      recipient=recipient)
        self.assertRaises(MessengerException,
                          messenger_user_profile.get_user_profile)
        mock_get.assert_called_with(
            'https://graph.facebook.com/v2.6/123',
            params={'access_token': '1234',
                    'fields' : 'first_name,last_name,profile_pic,locale,timezone,gender' }
        )
