// applications.test.js

global.fetch = require('node-fetch'); 
global.$ = jest.fn(() => ({
    modal: jest.fn(),
  }));
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

// Import the necessary modules if using ES6 imports, else use require.
// Assuming Jest is already set up with the ability to handle DOM-related methods such as `document.getElementById`.

// Mock fetch globally
global.fetch = jest.fn();

// Helper function to mock successful fetch response
function mockFetchSuccess(data) {
  return fetch.mockImplementationOnce(() =>
    Promise.resolve({
      json: () => Promise.resolve(data),
    })
  );
}

// Helper function to mock fetch failure
function mockFetchFailure(error) {
  return fetch.mockImplementationOnce(() => Promise.reject(error));
}

describe('getBadges', () => {
  // Reset the fetch mock before each test
  beforeEach(() => {
    fetch.mockClear();
    document.body.innerHTML = '<div id="test-role-id"></div>';
  });

  it('should fetch and display skill badges when data is returned', async () => {
    const fakeSkills = {
      skills: [
        { skill_name: 'JavaScript' },
        { skill_name: 'React' },
      ],
    };

    // Set up our fetch call to be successful
    mockFetchSuccess(fakeSkills);

    await getBadges('test-role-id');

    // Check if fetch was called correctly
    expect(fetch).toHaveBeenCalledTimes(1);
    expect(fetch).toHaveBeenCalledWith('http://localhost:5001/skills/role/test-role-id');

    // Check if badges were added to the DOM
    const badgesContainer = document.getElementById('test-role-id');
    expect(badgesContainer.innerHTML).toContain('<span class="badge badge-success">JavaScript</span>');
    expect(badgesContainer.innerHTML).toContain('<span class="badge badge-success">React</span>');
  });

  it('should handle the error when fetch fails', async () => {
    const consoleSpy = jest.spyOn(console, 'error');
    const errorMessage = 'Network error';

    // Set up our fetch call to fail
    mockFetchFailure(new Error(errorMessage));

    await getBadges('test-role-id');

    // Check that fetch was called
    expect(fetch).toHaveBeenCalledTimes(1);

    // Check that console.error was called with the error message
    expect(consoleSpy).toHaveBeenCalledWith('An error occured:', expect.any(Error));

    // Restore the original implementation of console.error if needed
    consoleSpy.mockRestore();
  });
});
