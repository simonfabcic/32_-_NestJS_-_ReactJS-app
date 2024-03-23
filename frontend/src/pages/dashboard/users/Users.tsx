import React, { useEffect } from 'react'
import useAxios from "../../utils/useAxios"


const Users = () => {
  let api = useAxios()

  // API REQUESTS -------------------------------------------------------------
  // --------------------------------------------------------------------------
  
  // Get all profiles
  useEffect(() => {
    getProfiles()
  }, [])
  let getProfiles = async () => {
    try {
      let response = await api.get('http://127.0.0.1:8000/core-api-v1/profiles/')
    } catch (err: any) {
      console.error("During getting 'Users', err occurred: ", err.message);
    }
  }


  // RETURN -------------------------------------------------------------------
  // --------------------------------------------------------------------------

  return (
    <>
      <div>Users</div>
      {/* TODO: Table of users */}
      <button>Add User</button>
      <table>
        <tr>
          <th>Email</th>
          <th>Full name</th>
          <th>Role</th>
          <th>Actions</th>
        </tr>
        <tr>
          <td>john@email.com</td>
          <td>John Doe</td>
          <td>Admin</td>
          <td>
            <button className='p-4 border border-red-500 rounded-sm'>Delete</button>
            <button className='p-4 border border-red-500 rounded-sm'>Edit</button>
          </td>
        </tr>
      </table>
      {/* TODO: page n of m */}
    </>
  )
}

export default Users