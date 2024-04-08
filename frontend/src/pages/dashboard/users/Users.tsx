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
    // username: string;
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
  // const [paginationOffset, setPaginationOffset] = useState(0)
  // const [paginationLimit, setPaginationLimit] = useState(20)
  const [loadingState, setLoadingState] = useState("Loading...")

  const [deleteButtonPressed, setDeleteButtonPressed] = useState(false)
  const [deleteButtonPressedOnUserId, setDeleteButtonPressedOnUserId] = useState(-1)

  let paginationOffset = 0
  let paginationPageSize = 20

  // API REQUESTS -------------------------------------------------------------
  // --------------------------------------------------------------------------
  
  // Get all profiles ---------------------------
  useEffect(() => {
    getProfiles()
  }, [])
  let getProfiles = async () => {
    try {
      let response = await api.get((`/shop-api-v1/profiles?offset=${paginationOffset}&page_size=${paginationPageSize}&sort_by=${sortingColumn}&sort_order=${sortOrder}`))
      console.log(response)
      if (response.status === 200) {
        setTableData(response.data)
        // console.log(response.data)
      }
    } catch (err: any) {
      console.error("During getting 'Profiles', err occurred: ", err.message);
      setLoadingState("Can't get profiles data. Contact admin...")
    }
  }

  // Delete profile -----------------------------
  let deleteProfile = async (id: number) => {
    try {
      let response = await api.delete((`/shop-api-v1/profile/${id}`))
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
      {(tableData.headers.length > 0 && tableData.rows.length > 0) ? 
        <table className="w-full text-center">
          <thead>
            <tr>
              <th>No.</th>
              {tableData.headers && tableData.headers.map((header) => (
                <th
                  key={header.label}
                >
                  {header.label}
                  {/* TODO: Add sorting functionality here */}
                  {/* {header.label + String.fromCharCode(160)}
                  {sortingColumn === header.key && sortOrder === "ASC" && <span> ▽</span>}
                  {sortingColumn === header.key && sortOrder === "DESC" && <span> △</span>}
                  {sortingColumn !== header.key && <span> △▽</span>} */}
                </th>
                ))}
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {tableData.rows && tableData.rows.map((row, index) => (
              <tr
                key={row.id}
                className={`
                  h-14
                  ${deleteButtonPressed && deleteButtonPressedOnUserId==row.id ? "bg-red-200" : "even:bg-gray-400"}
                `}
              >
                <td>{index+1}</td>
                {tableData.headers.map((header) => (
                  <td key={header.key}>
                    {/* {(row as Row)[header.key as keyof Row]} */}
                    {row.hasOwnProperty(header.key) ? row[header.key as keyof Row] : 'N/A'}
                  </td>
                ))}
                <td
                  className="space-x-2"
                >
                  {/* <p>{row.id}</p> */}
                  <button
                    className="px-3 py-1 bg-yellow-300 rounded"
                    onClick={() => navigate(`${row.id}`)}
                  >
                    Edit
                  </button>
                  <button
                    className="bg-red-500 hover:bg-red-600 text-white py-1 px-3 rounded"
                    onClick={() => {
                      deleteProfile(row.id)
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
                </td>
              </tr>
            ))}
          </tbody>
        </table>
        :
        <p className="font-bold">{loadingState}</p>
      }
      
      {/* TODO: page n of m */}
      {/* CONTINUE add pagination */}
    </>
  )
}

export default Users