import React, { useEffect, useState } from 'react'
import useAxios from "../../utils/useAxios"
import { useNavigate } from "react-router-dom";


const Users = () => {
  // INTERFACES ---------------------------------------------------------------
  // --------------------------------------------------------------------------

  interface Header {
    key: string;
    label: string;
    sorting: boolean;
  }
  
  interface Row {
    id:  number;
    email: string;
    full_name: string;
    role: string;
    username: string;
  }
  
  interface ApiResponseProfiles {
    headers: Header[];
    rows: Row[];
  }
  
  // VARIABLES ----------------------------------------------------------------
  // --------------------------------------------------------------------------
  
  let api = useAxios()
  const navigate = useNavigate()

  const [tableData, setTableData] = useState<ApiResponseProfiles>({headers:[], rows:[]})
  const [sortingColumn, setSortingColumn] = useState("full_name")
  const [sortOrder, setSortOrder] = useState("ASC")
  const [paginationOffset, setPaginationOffset] = useState(0)
  const [paginationLimit, setPaginationLimit] = useState(20)

  const [deleteButtonPressed, setDeleteButtonPressed] = useState(false)
  const [deleteButtonPressedOnUserId, setDeleteButtonPressedOnUserId] = useState(-1)

  // API REQUESTS -------------------------------------------------------------
  // --------------------------------------------------------------------------
  
  // Get all profiles ---------------------------
  useEffect(() => {
    getProfiles()
  }, [])
  let getProfiles = async () => {
    try {
      let response = await api.get((`/shop-api-v1/profiles?offset=${paginationOffset}&per_page=${paginationLimit}&sort_by=${sortOrder}&sort_order=${sortingColumn}`))
      // console.log(response)
      if (response.status === 200) {
        setTableData(response.data)
        // console.log(response.data)
      }
    } catch (err: any) {
      console.error("During getting 'Profiles', err occurred: ", err.message);
    }
  }

  // Delete profile -----------------------------
  let deleteProfile = async (username: string, id: number) => {
    try {
      let response = await api.delete((`/shop-api-v1/profile/${username}`))
      //console.log(response)
      if (response.status === 204) {
        setTableData(prevTableState => ({
          headers : prevTableState.headers,
          rows : prevTableState.rows.filter(row => row.id !== id)
        }))
      }
      // QUESTION how to create, that deleted row will disappear animated
    } catch (err: any) {
      console.error("During getting 'Deleting profile', err occurred: ", err.message);
    }
  }


  // RETURN -------------------------------------------------------------------
  // --------------------------------------------------------------------------

  return (
    <>
      <div>Users</div>
      <button
        className="px-4 py-2 bg-gray-400 rounded-md"
        onClick={() => navigate("add-new")}
      >
        Add User
      </button>
      <table className="w-full text-center">
        <thead>
          <tr>
            <th>No.</th>
            {tableData.headers && tableData.headers.map((header, index) => (
              <th
                key={index}
              >
                {header.label}
                {/* TODO: Add sorting functionality here */}
                {/* {header.label + String.fromCharCode(160)}
                {sortingColumn === header.key && sortOrder === "ASC" && <span> ▽</span>}
                {sortingColumn === header.key && sortOrder === "DSC" && <span> △</span>}
                {sortingColumn !== header.key && <span> △▽</span>} */}
              </th>
              ))}
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {tableData.rows && tableData.rows.map((row, index) => (
            <tr
              key={row.username}
              className={`
                
                h-14
                ${deleteButtonPressed && deleteButtonPressedOnUserId==row.id ? "bg-red-200" : "even:bg-gray-400"}
              `}
            >
              <td>{index+1}</td>
              {tableData.headers.map((header, index) => (
                <td key={index}>
                  {/* {(row as Row)[header.key as keyof Row]} */}
                  {row.hasOwnProperty(header.key) ? row[header.key as keyof Row] : 'N/A'}
                </td>
              ))}
              <td
                className="space-x-2"
              >
                <button
                  className="px-3 py-1 bg-yellow-300 rounded"
                  onClick={() => navigate(row.username)}
                >
                  Edit
                </button>
                <button
                  className="bg-red-500 hover:bg-red-600 text-white py-1 px-3 rounded"
                  onClick={() => {
                    deleteProfile(row.username, row.id)
                    setDeleteButtonPressedOnUserId(row.id)
                  }}
                  onMouseDown={() => {
                    setDeleteButtonPressed(true)
                    setDeleteButtonPressedOnUserId(row.id)
                  }}
                  onMouseUp={() => {
                    setDeleteButtonPressed(false)
                    setDeleteButtonPressedOnUserId(-1)
                  }}
                  onMouseLeave={() => setDeleteButtonPressed(false)}
                >
                  Delete
                </button>
              </td>{/* TODO */}
            </tr>
          ))}
        </tbody>
      </table>
      
      {/* TODO: page n of m */}
      {deleteButtonPressed}
      {deleteButtonPressedOnUserId}
    </>
  )
}

export default Users