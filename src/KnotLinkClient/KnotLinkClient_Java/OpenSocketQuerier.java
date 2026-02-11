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

import java.io.InputStream;
import java.io.PrintWriter;
import java.net.Socket;
import java.nio.charset.StandardCharsets;
import java.util.concurrent.CompletableFuture;
import java.util.logging.Logger;

public class OpenSocketQuerier {
    private static final String SERVER_IP = "127.0.0.1";
    private static final int QUERIER_PORT = 6376;
    private static final Logger LOGGER = Logger.getLogger(OpenSocketQuerier.class.getName());

    public static CompletableFuture<String> query(String appID, String openSocketID, String question) {
        return CompletableFuture.supplyAsync(() -> {
            try (Socket socket = new Socket(SERVER_IP, QUERIER_PORT);
                 PrintWriter out = new PrintWriter(socket.getOutputStream(), true);
                 InputStream in = socket.getInputStream()) {

                socket.setSoTimeout(5000);

                String packet = String.format("%s-%s&*&%s", appID, openSocketID, question);
                LOGGER.info(() -> "Sending query to KnotLink: " + question);
                out.print(packet);
                out.flush();

                byte[] buffer = new byte[4096];
                int bytesRead = in.read(buffer);

                if (bytesRead > 0) {
                    String response = new String(buffer, 0, bytesRead, StandardCharsets.UTF_8);
                    System.out.println("Received query response: " + response);
                    return response;
                } else {
                    System.out.println("Received no response from KnotLink server.");
                    return "ERROR: No response from KnotLink.";
                }

            } catch (Exception e) {
                System.out.println("Failed to query KnotLink server: " + e.getMessage());
                return "ERROR: Cannot connect to KnotLink. Ensure the service is running.";
            }
        });
    }
}