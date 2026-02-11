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

using System;
using System.IO;
using System.Net.Sockets;
using System.Text;
using System.Threading.Tasks;

namespace KnotLink
{
    public static class OpenSocketQuerier
    {
        public static async Task<string> QueryAsync(string appId, string openSocketId, string question, string host = "127.0.0.1", int port = 6376, int timeoutMs = 5000)
        {
            using var client = new TcpClient();
            client.ReceiveTimeout = timeoutMs;
            await client.ConnectAsync(host, port).ConfigureAwait(false);

            using NetworkStream stream = client.GetStream();
            string packet = appId + "-" + openSocketId + "&*&" + question;
            byte[] buffer = Encoding.UTF8.GetBytes(packet);
            await stream.WriteAsync(buffer, 0, buffer.Length).ConfigureAwait(false);
            await stream.FlushAsync().ConfigureAwait(false);

            byte[] respBuffer = new byte[4096];
            int read = await stream.ReadAsync(respBuffer, 0, respBuffer.Length).ConfigureAwait(false);
            if (read <= 0)
            {
                throw new IOException("No response from KnotLink.");
            }

            return Encoding.UTF8.GetString(respBuffer, 0, read);
        }
    }
}
