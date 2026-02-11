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
using System.Threading.Tasks;

namespace KnotLink
{
    public sealed class SignalSender : IAsyncDisposable, IDisposable
    {
        private readonly KlTcpClient _client;
        private string _appId;
        private string _signalId;

        public SignalSender(string appId, string signalId, string host = "127.0.0.1", int port = 6370)
        {
            _appId = appId;
            _signalId = signalId;
            _client = new KlTcpClient();
            _client.ConnectAsync(host, port).GetAwaiter().GetResult();
        }

        public void SetConfig(string appId, string signalId)
        {
            _appId = appId;
            _signalId = signalId;
        }

        public Task EmitAsync(string data)
        {
            if (string.IsNullOrEmpty(_appId) || string.IsNullOrEmpty(_signalId))
            {
                throw new InvalidOperationException("AppId and SignalId must be set before emitting.");
            }

            string sKey = _appId + "-" + _signalId + "&*&";
            return _client.SendAsync(sKey + data);
        }

        public void Dispose()
        {
            _client.Dispose();
        }

        public ValueTask DisposeAsync()
        {
            return _client.DisposeAsync();
        }
    }
}
