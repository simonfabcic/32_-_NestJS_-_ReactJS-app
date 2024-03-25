import React, { useEffect, useState } from 'react'
import useAxios from "../../utils/useAxios"


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
  }
  
  interface ApiResponseProfiles {
    headers: Header[];
    rows: Row[];
  }
  
  // VARIABLES ----------------------------------------------------------------
  // --------------------------------------------------------------------------
  
  let api = useAxios()
  const [tableData, setTableData] = useState<ApiResponseProfiles>({headers:[], rows:[]})
  const [sortingColumn, setSortingColumn] = useState("full_name")
  const [sortOrder, setSortOrder] = useState("ASC")
  const [paginationOffset, setPaginationOffset] = useState(0)
  const [paginationLimit, setPaginationLimit] = useState(20)

  // API REQUESTS -------------------------------------------------------------
  // --------------------------------------------------------------------------
  
  // Get all profiles ---------------------------
  useEffect(() => {
    getProfiles()
  }, [])
  let getProfiles = async () => {
    try {
      let response = await api.get((`http://127.0.0.1:8000/shop-api-v1/profiles?offset=${paginationOffset}&per_page=${paginationLimit}&sort_by=${sortOrder}&sort_order=${sortingColumn}`))
      console.log(response)
      if (response.status === 200) {
        setTableData(response.data)
      }

    } catch (err: any) {
      console.error("During getting 'Profiles', err occurred: ", err.message);
    }
  }


  // RETURN -------------------------------------------------------------------
  // --------------------------------------------------------------------------

  return (
    <>
      <div>Users</div>
      {/* TODO: Table of users */}
      <button>Add User</button>
      
      
      
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
              key={index}
              className="
                even:bg-gray-400
              "
            >
              <td>{index+1}</td>
              {tableData.headers.map((header, index) => (
                <td key={index}>
                  {/* {(row as Row)[header.key as keyof Row]} */}
                  {row.hasOwnProperty(header.key) ? row[header.key as keyof Row] : 'N/A'}
                </td>
              ))}
              <td>Actions...</td>{/* TODO */}
            </tr>
          ))}
        </tbody>
      </table>
      
      {/* TODO: page n of m */}
    </>
  )
}

export default Users