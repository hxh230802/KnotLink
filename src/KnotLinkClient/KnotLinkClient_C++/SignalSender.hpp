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

#ifndef SIGNALSENDER_HPP
#define SIGNALSENDER_HPP

#include <string>
#include "tcpclient.hpp"

class SignalSender {
public:
	SignalSender();
	~SignalSender();
	SignalSender(std::string APPID, std::string SignalID);
	void setConfig(std::string APPID, std::string SignalID);
	void emitt(std::string data);
	void emitt(std::string APPID, std::string SignalID, std::string data);
	
private:
	TcpClient* KLsender;
	std::string appID;
	std::string signalID;
	void init();
};

SignalSender::SignalSender() {
	init();
}

SignalSender::SignalSender(std::string APPID, std::string SignalID) : appID(APPID), signalID(SignalID) {
	init();
}


void SignalSender::init() {
	KLsender = new TcpClient();
	KLsender->connectToServer("127.0.0.1", 6370);
}

void SignalSender::setConfig(std::string APPID, std::string SignalID) {
	appID = APPID;
	signalID = SignalID;
}

void SignalSender::emitt(std::string data) {
	emitt(appID, signalID, data);
}

void SignalSender::emitt(std::string APPID, std::string SignalID, std::string data) {
	std::string s_key = APPID + "-" + SignalID;
	s_key += "&*&";
	// Create s_data by combining s_key and data
	std::string s_data = s_key + data;
	KLsender->sendData(s_data);
}

SignalSender::~SignalSender() {
	if (KLsender) {
		KLsender->stopHeartbeat();
		delete KLsender;
		KLsender = nullptr;
	}
}

#endif // SIGNALSENDER_HPP
