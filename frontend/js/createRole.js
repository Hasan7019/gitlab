var selectedSkillsId = []
const currentUser = 123456788
async function loadSkills() {

    try {
        const res = await fetch('http://localhost:5001/skills');
        const data = await res.json();
        for (let skill of data.data.skill) {
            document.getElementById("skillForm").innerHTML += `
            <div>
              <input type="checkbox" id="${skill.skill_id}" name="${skill.skill_name}" value="${skill.skill_id}">
              <label for="${skill.skill_id}">${skill.skill_name}</label>
              </div>
          `
        }
        const checkboxes = document.querySelectorAll('input[type="checkbox"]')
        const selectedSkills = document.getElementById('selected-skills')
        checkboxes.forEach(checkbox => {
            checkbox.addEventListener('change', () => {
                selectedSkillsId.length = 0
                const selectedCheckboxes = Array.from(checkboxes).filter(checkbox => {
                    if (checkbox.checked) {
                        selectedSkillsId.push(checkbox.value)
                    }
                    return checkbox.checked
                });
                const selectedSkillsText = selectedCheckboxes.map(checkbox => checkbox.labels[0].textContent).join(', ')
                selectedSkills.textContent = selectedSkillsText
            });
        });
    } catch (err) {
        console.error('An error occurred:', err)
    }
}

async function loadManagers() {
    try {
        const res = await fetch('http://localhost:5000/staff');
        const data = await res.json();
        for (let staff of data.data.staff) {
            document.getElementById("manager").innerHTML += `
            <option value=${staff.staff_id}>${staff.fname} ${staff.lname}</option>
          `
        }
    } catch (err) {
        console.error('An error occurred:', err)
    }
}

async function createListing() {
    const roleTitle = document.getElementById("role-title").value
    const roleDesc = document.getElementById("role-desc").value
    const id = await generateId()

    const roleData = {
        role_id: id,
        role_name: roleTitle,
        role_description: roleDesc,
        role_status: "active"
    }

    try {
        await fetch('http://localhost:5002/roles', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(roleData)
        })
    } catch (err) {
        console.error('An error occurred:', err)
    }

    for (skill of selectedSkillsId) {
        const roleSkill = {
            role_id: id,
            skill_id: parseInt(skill)
        }

        try {
            await fetch('http://localhost:5001/role-skill', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(roleSkill)
            })
        } catch (err) {
            console.error('An error occurred:', err)
        }
    }

    const listingDesc = document.getElementById("listing-desc").value
    const manager = document.getElementById("manager").value
    const openingDate = document.getElementById("opening-date").value
    const closingDate = document.getElementById("closing-date").value
    const currentDate = new Date().toISOString().split('T')[0]
    const listingId = await generateListingId()
    const listingData = {
        role_listing_id: listingId,
        role_id: id,
        role_listing_desc: listingDesc,
        role_listing_source: manager,
        role_listing_open: openingDate,
        role_listing_close: closingDate,
        role_listing_creator: currentUser,
        role_listing_ts_create: currentDate,
        role_listing_updater: currentUser,
        role_listing_ts_update: currentDate
    }

    try {
        await fetch('http://localhost:5002/role-listings', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(listingData)
        })
    } catch (err) {
        console.error('An error occurred:', err)
    }
}

async function generateId() {
    try {
        const res = await fetch('http://localhost:5002/roles')
        const data = await res.json()
        let id = 234567890 + data.data.role.length + 1;
        return id
    } catch (err) {
        console.error('An error occurred:', err)
    }
}

async function generateListingId() {
    try {
        const res = await fetch('http://localhost:5002/role-listings')
        const data = await res.json()
        let id = 123455 + data.data.listing.length + 1;
        return id
    } catch (err) {
        console.error('An error occurred:', err)
    }
}

loadSkills()
loadManagers()
