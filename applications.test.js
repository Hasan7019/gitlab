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


// You may need to import other modules or utilities depending on your setup
const {getLackingSkills }= require('./frontend/js/viewOpenRoles'); // Adjust the import path as necessary
global.fetch = jest.fn(); // Mocking fetch globally

beforeEach(() => {
  fetch.mockClear(); // Clear mock information between tests
});

it('returns skill names when the response code is 200', async () => {
  const staff_id = 'staff123';
  const listingId = 'listing123';
  const mockSkills = {
    code: 200,
    lacking_skills: [
      { skill_id: 'skill1' },
      { skill_id: 'skill2' },
    ],
  };
  const mockSkillNames = {
    code: 200,
    skill: {
      skill_name: 'Skill Name',
    },
  };

  // Mock the first fetch call
  fetch.mockResolvedValueOnce({
    json: () => Promise.resolve(mockSkills),
  });

  // Mock the subsequent fetch calls for each skill
  fetch.mockResolvedValue({
    json: () => Promise.resolve(mockSkillNames),
  });

  await expect(getLackingSkills(staff_id, listingId)).resolves.toEqual(['Skill Name', 'Skill Name']);

  // Check if fetch was called the correct number of times
  expect(fetch).toHaveBeenCalledTimes(1 + mockSkills.lacking_skills.length);

  // Check if fetch was called with the correct endpoints
  expect(fetch).toHaveBeenNthCalledWith(1, `http://localhost:5001/get-lacking-skills/${staff_id}/${listingId}`);
  mockSkills.lacking_skills.forEach((skill, index) => {
    expect(fetch).toHaveBeenNthCalledWith(2 + index, `http://localhost:5001/skills/${skill.skill_id}`);
  });
});

it('returns an empty array when the response code is not 200', async () => {
  const staff_id = 'staff123';
  const listingId = 'listing123';
  const mockSkills = {
    code: 404,
    lacking_skills: [],
  };

  // Mock the fetch call to simulate a non-200 response
  fetch.mockResolvedValueOnce({
    json: () => Promise.resolve(mockSkills),
  });

  await expect(getLackingSkills(staff_id, listingId)).resolves.toEqual([]);

  // Check if fetch was called only once
  expect(fetch).toHaveBeenCalledTimes(1);

  // Check if fetch was called with the correct endpoint
  expect(fetch).toHaveBeenCalledWith(`http://localhost:5001/get-lacking-skills/${staff_id}/${listingId}`);
});

//END OF FETCH SKILLS TEST

//BEGIN EDIT MODAL TEST

global.fetch = jest.fn(() => Promise.resolve({
  json: () => Promise.resolve({ /* Mocked response */ })
}));


const { openEditModal } = require('./frontend/js/viewOpenRoles'); 
// Mock global listings array
beforeEach(() => {
  // Set up the document body before each test
  document.body.innerHTML = `
    <input id="edit-role-description" />
    <input id="closing-date" />
  `;
  // Ensure listings is set before each test
  global.listings = [
    { role_id: '1', role_listing_desc: 'Description for role 1', role_listing_close: '2023-12-31T00:00:00Z' },
    { role_id: '2', role_listing_desc: 'Description for role 2', role_listing_close: '2024-01-31T00:00:00Z' },
    // ... other listings
  ];
});

describe('openEditModal', () => {
  it('sets the correct values in the modal', () => {
    // Now we use 'role1' or 'role2' which we know exist in the global listings
    openEditModal('role1');

    const roleDescription = document.getElementById('edit-role-description').value;
    const closingDate = document.getElementById('closing-date').value;

    // Adjust these expected values based on the role_id you used above
    expect(roleDescription).toBe('Description for role 1');
    expect(closingDate).toBe(new Date('2023-12-31T00:00:00Z').toISOString().split('T')[0]);
  });
});



// Assuming getStaffName is in a file named staff.js
const { getStaffName } = require('./frontend/js/viewOpenRoles');

// Mocking the global fetch function
global.fetch = jest.fn();

beforeEach(() => {
  // Clear all instances and calls to constructor and all methods:
  fetch.mockClear();
});

describe('getStaffName', () => {
  it('returns the correct full name of a staff member', async () => {
    // Mock the fetch response
    fetch.mockResolvedValue({
      json: () => Promise.resolve({
        staff: {
          fname: 'John',
          lname: 'Doe'
        }
      })
    });

    // staff_id to test
    const staff_id = '123';

    // Call the function with the mock staff_id
    const fullName = await getStaffName(staff_id);

    // Assertions to check if the full name is correct
    expect(fullName).toBe('John Doe');

    // Check if fetch was called with the correct URL
    expect(fetch).toHaveBeenCalledWith('http://localhost:5000/staff/' + staff_id);
  });

  // add more tests here?? e.g:
  // - What happens if the fetch call fails?
  // - What happens if the response does not contain a staff object?
  // - etc.
});

// Assuming getStaffSkills is in a file named staffSkills.js
// const { getStaffSkills } = require('./frontend/js/viewOpenRoles');

// // Mocking the global fetch function
// global.fetch = jest.fn();

// beforeEach(() => {
//   // Clear all instances and calls to constructor and all methods:
//   fetch.mockClear();
// });

// describe('getStaffSkills', () => {
//   it('returns active skills for a staff member', async () => {
//     // Mock the responses for staff skills and individual skill info
//     fetch
//       .mockResolvedValueOnce({ // First call to fetch for staff skills
//         json: () => Promise.resolve({
//           code: 200,
//           skills: [
//             { skill_id: '1', ss_status: 'active' },
//             { skill_id: '2', ss_status: 'inactive' },
//             { skill_id: '3', ss_status: 'active' }
//           ]
//         })
//       })
//       .mockResolvedValueOnce({ // Second call to fetch for the first skill details
//         json: () => Promise.resolve({
//           code: 200,
//           skill: { skill_name: 'Skill One' }
//         })
//       })
//       .mockResolvedValueOnce({ // Third call to fetch for the second skill details (skipped because inactive)
//         json: () => Promise.resolve({})
//       })
//       .mockResolvedValueOnce({ // Fourth call to fetch for the third skill details
//         json: () => Promise.resolve({
//           code: 200,
//           skill: { skill_name: 'Skill Three' }
//         })
//       });

//     // staff_id to test
//     const staff_id = 'staff123';
//     // Call the function with the mock staff_id
//     const skillNames = await getStaffSkills(staff_id);

//     // Assertions to check if the skill names array is correct
//     expect(skillNames).toEqual(['Skill One', 'Skill Three']);

//     // Check if fetch was called with the correct URLs
//     expect(fetch).toHaveBeenNthCalledWith(1, 'http://localhost:5001/skills/staff/' + staff_id);
//     expect(fetch).toHaveBeenNthCalledWith(2, 'http://localhost:5001/skills/1');
//     expect(fetch).toHaveBeenNthCalledWith(3, 'http://localhost:5001/skills/3');

//     // Since skill 2 is inactive, there should be no fetch call for its details
//     expect(fetch).toHaveBeenCalledTimes(3);
//   });

// });


// //GET APPLICATION ID

// // require('jest-fetch-mock').enableMocks();

// // const getApplicationId = require('./frontend/js/viewOpenRoles'); // Adjust the path to where your function is exported

// // describe('getApplicationId function', () => {
// //   beforeEach(() => {
// //     fetch.resetMocks();
// //   });

// //   it('returns the default ID when a 404 code is received', async () => {
// //     fetch.mockResponseOnce(JSON.stringify({ code: 404 }));
// //     const appId = await getApplicationId();
// //     expect(appId).toEqual(123456);
// //   });

// //   it('calculates and returns the correct ID when a non-404 code is received', async () => {
// //     const mockApplications = { data: { application: ['app1', 'app2', 'app3'] } };
// //     fetch.mockResponseOnce(JSON.stringify({ code: 200, ...mockApplications }));
// //     const appId = await getApplicationId();
// //     expect(appId).toEqual(123456 + mockApplications.data.application.length);
// //   });

// //   it('handles exceptions for network errors', async () => {
// //     fetch.mockReject(new Error('fake network error'));
// //     console.error = jest.fn(); // Mock console.error

// //     await getApplicationId();
    
// //     // Check if console.error was called with the correct message
// //     expect(console.error).toHaveBeenCalledWith('An error occurred:', expect.any(Error));
// //   });
// // });


// //WITHDRAW
// const { withdraw } = require('./frontend/js/viewOpenRoles'); // Ensure this path is correct.

// // Enable fetch mocking
// require('jest-fetch-mock').enableMocks()

// describe('withdraw', () => {
//   beforeEach(() => {
//     fetch.resetMocks();
//   });

//   it('sends a withdrawal request for a specific application', async () => {
//     // Arrange
//     const role_app_id = '123';
//     const expectedUrl = `http://localhost:5002/role-applications/${role_app_id}`;
//     const expectedBody = JSON.stringify({ role_app_status: "withdrawn" });

//     fetch.mockResponseOnce(JSON.stringify({ status: 'success' })); // Mock a successful response

//     // Act
//     await withdraw(role_app_id);

//     // Assert
//     expect(fetch).toHaveBeenCalledTimes(1);
//     expect(fetch).toHaveBeenCalledWith(expectedUrl, {
//       method: 'PUT',
//       headers: { 'Content-Type': 'application/json' },
//       body: expectedBody
//     });
//   });

//   it('handles exceptions thrown during the fetch operation', async () => {
//     // Arrange
//     const role_app_id = '123';
//     const errorMessage = 'Network error';

//     fetch.mockRejectOnce(new Error(errorMessage)); // Mock a network error

//     // Act
//     await withdraw(role_app_id);

//     // Assert
//     // Check if console.error was called with the correct error
//     // For this, you might need to mock console.error before the test
//     const consoleSpy = jest.spyOn(console, 'error');
//     expect(consoleSpy).toHaveBeenCalledWith(expect.any(Error));
//   });
// });
