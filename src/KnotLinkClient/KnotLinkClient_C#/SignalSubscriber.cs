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
    public sealed class SignalSubscriber : IAsyncDisposable, IDisposable
    {
        private readonly KlTcpClient _client;
        private readonly string _appId;
        private readonly string _signalId;
        private readonly string _host;
        private readonly int _port;

        public Func<string, Task>? OnSignalAsync { get; set; }

        public SignalSubscriber(string appId, string signalId, string host = "127.0.0.1", int port = 6372)
        {
            _appId = appId;
            _signalId = signalId;
            _host = host;
            _port = port;

            _client = new KlTcpClient();
            _client.OnDataReceivedAsync = HandleSignalAsync;

            ConnectAndSubscribe();
        }

        private void ConnectAndSubscribe()
        {
            _client.ConnectAsync(_host, _port).GetAwaiter().GetResult();
            SubscribeAsync().GetAwaiter().GetResult();
        }

        private async Task SubscribeAsync()
        {
            string key = _appId + "-" + _signalId;
            await _client.SendAsync(key).ConfigureAwait(false);
        }

        private Task HandleSignalAsync(string data)
        {
            if (OnSignalAsync != null)
            {
                return OnSignalAsync(data);
            }

            return Task.CompletedTask;
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
