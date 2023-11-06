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


// Assuming updateRoleListing.js contains the function you want to test
const { updateRoleListing } = require('./frontend/js/viewOpenRoles');

// Mock global.fetch
global.fetch = jest.fn();

// Mock the modal hide function (using jQuery in your function)
$.fn.modal = jest.fn();

// Mock global document object
document.getElementById = jest.fn();

// Mock global.window object
global.window = { currentRoleId: '123' };

describe('updateRoleListing', () => {
  beforeEach(() => {
    fetch.mockClear();
    document.getElementById.mockClear();
    $.fn.modal.mockClear();
    window.currentRoleId = '123'; // Reset currentRoleId before each test if needed
  });

  it('sends PUT request with the correct data', async () => {
    // Mocking DOM element values
    document.getElementById.mockImplementation((id) => {
      if (id === 'edit-role-description') {
        return {
          value: 'Updated Description',
        };
      }
      if (id === 'closing-date') {
        return {
          value: '2023-12-31',
        };
      }
      return null;
    });

    // Mock successful response
    fetch.mockResolvedValue({
      ok: true, // simulate success response
    });

    // Assume listings is available in the scope, if not you will have to mock it accordingly
    const listings = [
      { role_id: '123', role_listing_id: '456' }
    ];

    await updateRoleListing(listings); // If listings is a parameter in the actual function

    // Check that fetch was called
    expect(fetch).toHaveBeenCalledWith('http://localhost:5002/role-listings/456', {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        "role_listing_desc": 'Updated Description',
        "role_listing_close": '2023-12-31',
      })
    });

    // Check that the modal was hidden
    expect($.fn.modal).toHaveBeenCalledWith('hide');
  });

  it('handles exceptions', async () => {
    fetch.mockRejectedValue(new Error('Async error'));

    await expect(updateRoleListing()).rejects.toThrow('Async error');
  });
});
