// applications.test.js
const { applyAgain } = require('./applications'); // ensure the path is correct

// Mock fetch before your test cases
global.fetch = jest.fn(() => Promise.resolve({
  json: () => Promise.resolve({ success: true }),
}));

beforeEach(() => {
  // clear  mock before each test
  fetch.mockClear();
});

test('applyAgain makes a PUT request with the correct data', async () => {
  const role_app_id = '123';

  await applyAgain(role_app_id);

  // check if fetch was called
  expect(fetch).toHaveBeenCalledTimes(1);
  expect(fetch).toHaveBeenCalledWith(
    `http://localhost:5002/role-applications/${role_app_id}`,
    {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ role_app_status: "applied" }),
    }
  );
});
