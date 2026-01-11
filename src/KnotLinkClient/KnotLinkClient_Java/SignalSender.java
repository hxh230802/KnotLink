public class SignalSender {
    private TcpClient KLsender;
    private String appID;
    private String signalID;
    private boolean connected;

    public SignalSender(String APPID, String SignalID) {
        this.appID = APPID;
        this.signalID = SignalID;
        init();
    }

    public void setConfig(String APPID, String SignalID) {
        this.appID = APPID;
        this.signalID = SignalID;
    }

    private void init() {
        KLsender = new TcpClient();
        connected = KLsender.connectToServer("127.0.0.1", 6378);
        if (!connected) {
            System.err.println("SignalSender failed to connect to KnotLink server.");
        }
    }

    public void emitt(String data) {
        if (appID == null || signalID == null) {
            System.err.println("APPID and SignalID must be defined.");
            return;
        }
        if (!connected) {
            System.err.println("SignalSender is not connected; cannot emit signal.");
            return;
        }
        String s_key = appID + "-" + signalID + "&*&";
        String s_data = s_key + data;
        KLsender.sendData(s_data);
    }

    public void close() {
        if (KLsender != null) {
            KLsender.close();
            connected = false;
        }
    }
}