// applications.test.js
const { applyAgain } = require('./frontend/js/viewOpenRoles');

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



const { fetchApplications } =  require('./frontend/js/viewOpenRoles');

// Mock fetch globally
global.fetch = jest.fn();

describe('fetchApplications', () => {
  beforeEach(() => {
    fetch.mockClear();
  });

  it('fetches applications correctly', async () => {
    const listingId = '123';
    const mockApplications = [{ id: 'app1' }, { id: 'app2' }];

    fetch.mockResolvedValue({
      json: () => Promise.resolve({ role_applications: mockApplications }),
    });

    const applications = await fetchApplications(listingId);

    // Check that fetch was called with the correct URL
    expect(fetch).toHaveBeenCalledWith(
      `http://localhost:5002/role-applications/listing/${listingId}`
    );

    // Check that the expected data was returned from the function
    expect(applications).toEqual(mockApplications);
  });

  it('handles exceptions', async () => {
    const listingId = '123';
    fetch.mockRejectedValue(new Error('Async error'));

    await expect(fetchApplications(listingId)).rejects.toThrow('Async error');
  });
});
