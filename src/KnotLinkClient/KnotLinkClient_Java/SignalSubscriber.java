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

public class SignalSubscriber {
    private TcpClient KLsubscriber;
    private final String appID;
    private final String signalID;

    // 定义一个回调接口
    public interface SignalListener {
        void onSignalReceived(String data);
    }

    private SignalListener signalListener;

    public SignalSubscriber(String appID, String signalID) {
        this.appID = appID;
        this.signalID = signalID;
    }

    public void setSignalListener(SignalListener listener) {
        this.signalListener = listener;
    }

    public void start() {
        if (signalListener == null) {
            System.err.println("SignalListener must be set before starting.");
            return;
        }
        KLsubscriber = new TcpClient();
        // SignalSubscriber 连接到端口 6372
        if (KLsubscriber.connectToServer("127.0.0.1", 6372)) {
            // 设置数据接收监听器
            KLsubscriber.setDataReceivedListener(data -> {
                System.out.println("DEBUG: Raw data received from KnotLink: " + data);
                signalListener.onSignalReceived(data);
            });

            // 发送订阅请求
            String s_key = appID + "-" + signalID;
            KLsubscriber.sendData(s_key);
            System.out.println("SignalSubscriber started and subscribed to " + s_key + ".");
        } else {
            System.out.println("SignalSubscriber failed to start.");
        }
    }

    public void stop() {
        if (KLsubscriber != null) {
            KLsubscriber.close();
            System.out.println("SignalSubscriber stopped.");
        }
    }
}