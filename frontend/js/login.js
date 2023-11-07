document.addEventListener("DOMContentLoaded", function () {
  const form = document.querySelector("form")

  form.addEventListener("submit", async function (event) {
    event.preventDefault();

    const email = document.getElementById("email").value
    const password = document.getElementById("password").value

    try {
      const res = await fetch("http://localhost:5000/staff/email/" + email)
      const data = await res.json()
      if (data.code === 200) {
        const staff = data.staff
        if (staff.sys_role === "manager" || staff.sys_role === "hr") {
          localStorage.setItem("userType", staff.sys_role)
        } else {
          localStorage.setItem("userType", staff.staff_id)
        }
        localStorage.setItem("userId", staff.staff_id)
      }
      window.location.href = "viewOpenRoles.html"
    } catch (error) {
      console.error("Error occurred while fetching user role:", error)
    }
  })
})
