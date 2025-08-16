// Copyright (C) 2025 HXH
//
// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
//
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with this program.  If not, see <https://www.gnu.org/licenses/>.

#ifndef SIGNAL_SUBSCRIBER_HPP
#define SIGNAL_SUBSCRIBER_HPP

#include <string>
#include "TcpClient.hpp"

class SignalSubscriber {
public:
	SignalSubscriber(const std::string& APPID, const std::string& SignalID) : appID(APPID), signalID(SignalID) {
		KLsubscriber = new TcpClient();
		KLsubscriber->connectToServer("127.0.0.1", 6372);
		KLsubscriber->setOnDataReceivedCallback(std::bind(&SignalSubscriber::handleReceivedData, this, std::placeholders::_1));
		while(!KLsubscriber->running){
		}
		subscribe(appID,signalID);
	}
	
	~SignalSubscriber() {
		
		stop();
		delete KLsubscriber;
	}
	
	void subscribe(const std::string& APPID, const std::string& SignalID) {
		appID = APPID;
		signalID = SignalID;
		std::string s_key = appID + "-" + signalID;
		KLsubscriber->sendData(s_key);
	}
	
	void start() {
		// The readData method is already called in TcpClient's thread
	}
	
	void stop() {
		std::cout<<555;
		KLsubscriber->stopHeartbeat();
		delete KLsubscriber;
	}
	
	void setOnDataReceivedCallback(const std::function<void(const std::string&)>& callback) {
		onDataReceivedCallback = callback;
	}
	
private:
	TcpClient* KLsubscriber;
	std::string appID;
	std::string signalID;
	std::function<void(const std::string&)> onDataReceivedCallback;
	
	void handleReceivedData(const std::string& data) {
		if (data == "heartbeat_response") {
			return;
		}
		if (onDataReceivedCallback) {
			onDataReceivedCallback(data);
		}
	}
};

#endif // SIGNAL_SUBSCRIBER_HPP
