import test from 'node:test';
import assert from 'node:assert/strict';
import { apiFetch, apiErrorMessage } from './api.js';

test('dashboard uses authenticated identity without username in URL', async () => {
    const originalFetch = globalThis.fetch;
    const originalStorage = globalThis.localStorage;
    try {
        globalThis.localStorage = { getItem: () => 'test-token' };
        globalThis.fetch = async (url, options) => {
            assert.equal(url, '/api/dashboard/stats/me');
            assert.equal(options.headers.get('Authorization'), 'Bearer test-token');
            return { ok: true };
        };
        assert.equal((await apiFetch('/dashboard/stats/me', { authenticated: true })).ok, true);
    } finally {
        globalThis.fetch = originalFetch;
        globalThis.localStorage = originalStorage;
    }
});

test('validation responses are readable', () => {
    assert.equal(apiErrorMessage({ detail: [{ msg: 'Invalid email' }] }, 'failed'), 'Invalid email');
    assert.equal(apiErrorMessage({ detail: 'Duplicate account' }, 'failed'), 'Duplicate account');
    assert.equal(apiErrorMessage({}, 'failed'), 'failed');
});
