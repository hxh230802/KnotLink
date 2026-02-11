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
    public sealed class OpenSocketResponser : IAsyncDisposable, IDisposable
    {
        private readonly KlTcpClient _client;
        private readonly string _appId;
        private readonly string _openSocketId;
        private readonly string _host;
        private readonly int _port;
        private bool _registered;

        public Func<string, Task<string>>? OnQuestionAsync { get; set; }

        public OpenSocketResponser(string appId, string openSocketId, string host = "127.0.0.1", int port = 6378)
        {
            _appId = appId;
            _openSocketId = openSocketId;
            _host = host;
            _port = port;
            _client = new KlTcpClient();
            _client.OnDataReceivedAsync = HandleDataAsync;

            ConnectAndRegister();
        }

        private void ConnectAndRegister()
        {
            _client.ConnectAsync(_host, _port).GetAwaiter().GetResult();
            RegisterAsync().GetAwaiter().GetResult();
        }

        private async Task RegisterAsync()
        {
            string key = _appId + "-" + _openSocketId;
            await _client.SendAsync(key).ConfigureAwait(false);
        }

        private async Task HandleDataAsync(string data)
        {
            if (!_registered && data == _appId + "-" + _openSocketId)
            {
                _registered = true;
                return;
            }

            string[] parts = data.Split(new[] { "&*&" }, 2, StringSplitOptions.None);
            if (parts.Length != 2)
            {
                return;
            }

            string questionId = parts[0];
            string payload = parts[1];
            string reply = OnQuestionAsync != null
                ? await OnQuestionAsync(payload).ConfigureAwait(false)
                : string.Empty;

            string response = questionId + "&*&" + reply;
            await _client.SendAsync(response).ConfigureAwait(false);
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
