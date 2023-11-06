let listings
let skillsFilter = []
const userType = "123456789"

async function fetchListings () {
  try {
    const res = await fetch('http://localhost:5002/role-listings')
    const data = await res.json()
    listings = data.data.listing
    document.getElementById("num-jobs").innerText = listings.length + " Jobs Listed"
    for (const postObj of data.data.listing) {
      document.getElementById("job-listings").innerHTML += `
        <li class="job-listing d-block d-sm-flex pb-3 pb-sm-0 align-items-center">
          <div class="job-listing-about d-sm-flex custom-width w-100 justify-content-between mx-4 text-dark">
            <div class="job-listing-logo">
              ${postObj.role_id}
            </div>
            <div id="${postObj.role_id}" class="job-listing-position custom-width w-50 mb-3 mb-sm-0" data-toggle="modal" data-target="#job-modal" style="cursor: pointer" data-id="${postObj.role_id}" onclick="showModal(${postObj.role_id}, ${postObj.role_listing_id}); getModalBadges(${postObj.role_id})">
              <h2>${postObj.role_listing_desc}</h2>
            </div>
            <div class="job-listing-location mb-3 mb-sm-0 custom-width w-25">
              Closing on: ${postObj.role_listing_close} 
            </div>
            <div id="button-${postObj.role_listing_id}">
            </div>
          </div>
        </li>
      `
      if (userType === "admin") {
        document.getElementById("button-" + postObj.role_listing_id).innerHTML += `
          <button class="btn btn-primary btn-sm" data-toggle="modal" data-target="#edit-modal" onclick="openEditModal(${postObj.role_id})">Edit</button>
        `
      } else if (userType !== "manager") {
        await loadButton(postObj.role_listing_id)
      }
      getBadges(postObj.role_id)
    }
    if (data.code === 200) {
      return data.data.listing
    } else {
      console.error('Failed to fetch listings.')
    }
  } catch (err) {
    console.error('An error occurred:', err)
  }
}

async function loadButton (roleListingId) {
  try {
    const res = await fetch('http://localhost:5002/role-applications/' + roleListingId + '/' + userType)
    const data = await res.json()
    const application = data.role_application
    if (data.code === 404) {
      document.getElementById("button-" + roleListingId).innerHTML += `
          <button class="btn btn-primary btn-sm" onclick="apply(${userType}, ${roleListingId})">Apply</button>
        `
    } else if (application.role_app_status == "withdrawn") {
      document.getElementById("button-" + roleListingId).innerHTML += `
          <button class="btn btn-primary btn-sm" onclick="applyAgain(${application.role_app_id})">Apply</button>
        `
    }
    else {
      document.getElementById("button-" + roleListingId).innerHTML += `
        <button class="btn btn-primary btn-sm" onclick="withdraw(${application.role_app_id})">Withdraw</button>
      `
    }
  } catch (err) {
    console.error('An error occured:', err)
  }
}

async function withdraw(roleAppId) {
  const updatedData = {
    role_app_status: "withdrawn"
  }

  try {
    await fetch('http://localhost:5002/role-applications/' + roleAppId, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(updatedData)
    })
  } catch (err) {
    console.error(err)
  }
}

async function applyAgain(roleAppId) {
  const updatedData = {
    role_app_status: "applied"
  }

  try {
    await fetch('http://localhost:5002/role-applications/' + roleAppId, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(updatedData)
    })
  } catch (err) {
    console.error(err)
  }
}

async function getBadges(roleId) {
  try {
    const res = await fetch('http://localhost:5001/skills/role/' + roleId)
    const data = await res.json()
    if (data.skills.length != 0) {
      for (skill of data.skills) {
        document.getElementById(roleId).innerHTML += `
          <span class="badge badge-success">${skill.skill_name}</span>
        `
      }
    }
  } catch (err) {
    console.error('An error occured:', err)
  }
}

async function getModalBadges(roleId) {
  try {
    const res = await fetch('http://localhost:5001/skills/role/' + roleId)
    const data = await res.json()
    document.getElementById("modal-badge").innerHTML = ""
    if (data.skills.length != 0) {
      for (const skill of data.skills) {
        document.getElementById("modal-badge").innerHTML += `
          <span class="badge badge-success text-white">${skill.skill_name}</span>
        `
      }
    }
  } catch (err) {
    console.error('An error occured:', err)
  }
}

async function apply (id, roleListingId) {
  const applicationData = {
    role_app_id: await getApplicationId(),
    role_listing_id: roleListingId,
    staff_id: id,
    role_app_status: "applied",
    role_app_ts_create: new Date().toISOString().split('T')[0]
  }

  try {
    await fetch('http://localhost:5002/role-applications', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(applicationData)
    })
  } catch (err) {
    console.error(err)
  }
}

async function getApplicationId () {
  try {
    const res = await fetch('http://localhost:5002/role-applications');
    const data = await res.json()
    if (data.code === 404) {
      return 123456
    } else {
      return 123456 + data.data.application.length
    }
  } catch (err) {
    console.error('An error occurred:', err)
  }
}

async function fetchRole (id) {
  try {
    const res = await fetch('http://localhost:5002/roles/' + id)
    const data = await res.json()

    if (data.code === 200) {
      return data.role
    } else {
      console.error('Failed to fetch role.')
    }
  } catch (err) {
    console.error('An error occurred:', err)
  }
}

async function fetchSkills () {
  try {
    const res = await fetch('http://localhost:5001/skills')
    const data = await res.json()
    if (data.data.skill.length != 0) {
      var selectSkills = document.getElementById("skills-select")
      for (const skill of data.data.skill) {
        selectSkills.innerHTML += `
          <option value="${skill.skill_id}">${skill.skill_name}</option>
        `
      }
      $(selectSkills).selectpicker('refresh')
      document.getElementById("skills-select").addEventListener("change", function () {
        skillsFilter = Array.from(selectSkills.selectedOptions).map(option => option.value)
      })
    }
  } catch (err) {
    console.error('An error occured:', err)
  }
}

fetchListings()
fetchSkills()

async function showModal (jobId, listingId) {
  if (userType === "manager") {
    document.getElementById("modal-body").innerHTML = `
      <div class="card">
        <div class="card-body">
          <h5 class="card-title" id="modal-job-title"></h5>
          <p class="card-text" id="modal-job-description"></p>
        </div>
      </div>
    `
    fetchApplications(listingId).then(applications => {
      for (const application of applications) {
        getStaffName(application.staff_id).then(name => {
          document.getElementById("modal-body").innerHTML += `
              <div class="card">
                <div class="card-body" id=modal-${application.staff_id}>
                  ${name}
                </div>
              </div>
            `
        })
        getStaffSkills(application.staff_id).then(skills => {
          for (const skill of skills) {
            document.getElementById("modal-" + application.staff_id).innerHTML += `
              <span class="badge badge-success text-white">${skill}</span>
            `
          }
        })
      }
    })
  }

  if (userType !== "manager" && userType !== "admin") {
    try {
      document.getElementById("show-lacking-skills").innerHTML = `
        <div id="your-skills">
          <span>Your skills:</span>
        </div>
        <div id="lacking-skills">
          <span>Lacking skills:</span>
        </div>
      `
      document.getElementById("your-skills").innerHTML = "<span>Your skills:</span>"
      document.getElementById("lacking-skills").innerHTML = "<span>Lacking skills:</span>"
      getStaffSkills(userType).then(skills => {

        for (skill of skills) {
          document.getElementById("your-skills").innerHTML += `
              <span class="badge badge-success text-white">${skill}</span>
            `
        }
        getLackingSkills(userType, listingId).then(lackingSkills => {
          for (lackingSkill of lackingSkills) {
            document.getElementById("lacking-skills").innerHTML += `
              <span class="badge badge-danger text-white">${lackingSkill}</span>
            `
          }
        })
      })

    } catch (err) {
      console.error(err)
    }
  }

  fetchRole(jobId).then(role => {
    const jobTitleElement = document.getElementById('modal-job-title')
    const jobDescriptionElement = document.getElementById('modal-job-description')
    jobTitleElement.textContent = role.role_name
    jobDescriptionElement.textContent = role.role_description

    $('#job-modal').modal('show')
  })
}

async function getStaffName (staffId) {
  const res = await fetch('http://localhost:5000/staff/' + staffId)
  const data = await res.json()
  return data.staff.fname + " " + data.staff.lname
}

async function getStaffSkills(staffId) {
  let names = []
  const res = await fetch('http://localhost:5001/skills/staff/' + staffId)
  const data = await res.json()
  if (data.code == 200) {
    for (const skill of data.skills) {
      if (skill.ss_status == 'active') {
        const res2 = await fetch('http://localhost:5001/skills/' + skill.skill_id)
        const data2 = await res2.json()
        if (data2.code === 200) {
          names.push(data2.skill.skill_name)
        }
      }
    }
  }
  return names
}

async function getLackingSkills (staffId, listingId) {
  const names = []
  const res = await fetch("http://localhost:5001/get-lacking-skills/" + staffId + "/" + listingId)
  const data = await res.json()
  if (data.code === 200) {
    for (skill of data.lacking_skills) {
      const res2 = await fetch('http://localhost:5001/skills/' + skill.skill_id)
      const data2 = await res2.json()
      if (data2.code == 200) {
        names.push(data2.skill.skill_name)
      }
    }
  }
  return names
}

async function fetchApplications (listingId) {
  const res = await fetch('http://localhost:5002/role-applications/listing/' + listingId)
  const data = await res.json()
  return data.role_applications
}

function openEditModal (roleId) {
  window.currentRoleId = roleId
  const role = listings.find(item => item.role_id === roleId)
  document.getElementById("edit-role-description").value = role.role_listing_desc
  document.getElementById("closing-date").value = new Date(role.role_listing_close).toISOString().split('T')[0]
}

async function updateRoleListing () {
  const updatedRoleDescription = document.getElementById("edit-role-description").value
  const closing_date = document.getElementById("closing-date").value
  const roleId = window.currentRoleId

  const role = listings.find(item => item.role_id === roleId)
  const toUpdate = {
    "role_listing_desc": updatedRoleDescription,
    "role_listing_close": closing_date
  }

  try {
    await fetch('http://localhost:5002/role-listings/' + role.role_listing_id, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(toUpdate)
    })
  } catch (error) {
    console.error(err)
  }
  $('#edit-modal').modal('hide')
}


async function searchListing () {
  let searchVal = document.getElementById("search").value
  let filteredListings = listings.filter(function (l) {
    return l.role_listing_desc.toLowerCase().includes(searchVal.toLowerCase())
  })

  let dateFilter = document.getElementById("date-filter-select").value
  const currentDate = new Date()

  filteredListings = filteredListings.filter(function (listing) {
    const closingDate = new Date(listing.role_listing_close)
    return closingDate >= currentDate
  })

  if (skillsFilter.length != 0) {
    try {
      for (var i = 0; i < filteredListings.length; i++) {
        var listing = filteredListings[i]
        const res = await fetch('http://localhost:5001/skills/role/' + listing.role_id)
        const data = await res.json()
        var toRemove = true
        if (data.skills.length != 0) {
          for (skill of data.skills) {
            if (skillsFilter.includes(skill.skill_id.toString())) {
              toRemove = false
            }
          }
        }
        if (toRemove) {
          filteredListings.splice(i--, 1)
        }
      }
    } catch (err) {
      console.error(err)
    }
  }

  if (dateFilter === "closingSoon") {
    filteredListings.sort(function (a, b) {
      return new Date(a.role_listing_close) - new Date(b.role_listing_close)
    })
  } else if (dateFilter === "latest") {
    filteredListings.sort(function (a, b) {
      return new Date(b.role_listing_ts_create) - new Date(a.role_listing_ts_create)
    })
  }

  document.getElementById("job-listings").innerHTML = ''
  for (let listing of filteredListings) {
    document.getElementById("job-listings").innerHTML += `
        <li class="job-listing d-block d-sm-flex pb-3 pb-sm-0 align-items-center" data-toggle="modal" data-target="#job-modal" style="cursor: pointer" data-id="${listing.role_id}" onclick="showModal(${listing.role_id}, ${listing.role_listing_id})">
          <div class="job-listing-about d-sm-flex custom-width w-100 justify-content-between mx-4 text-dark">
            <div class="job-listing-logo">
              ${listing.role_id}
            </div>
            <div id="${listing.role_id}" class="job-listing-position custom-width w-50 mb-3 mb-sm-0">
              <h2>${listing.role_listing_desc}</h2>
            </div>
            <div class="job-listing-location mb-3 mb-sm-0 custom-width w-25">
              Closing on: ${listing.role_listing_close} 
            </div>
          </div>
        </li>
      `
    if (userType == "admin") {
      document.getElementById("button-" + listing.role_listing_id).innerHTML += `
          <button class="btn btn-primary btn-sm" data-toggle="modal" data-target="#edit-modal" onclick="openEditModal(${listing.role_id})">Edit</button>
        `
    } else if (userType != "manager") {
      await loadButton(listing.role_listing_id)
    }
    getBadges(listing.role_id)
  }
}

