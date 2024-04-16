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
    pagination_description: {
      page: number;
      total_pages: number;
      sort_order: "ASC" | "DESC";
      sort_by: string;
      total_records: number;
      prev_page: number | null;
      next_page: number | null;
      page_size: number;
    }
  }
  
  // VARIABLES ----------------------------------------------------------------
  // --------------------------------------------------------------------------
  
  let api = useAxios()
  const navigate = useNavigate()

  const [tableData, setTableData] = useState<ApiResponseProfiles>({
    headers:[],
    rows:[],
    pagination_description:{
      page: 0,
      total_pages: 0,
      sort_order: "ASC",
      sort_by: "",
      total_records: 0,
      prev_page: null,
      next_page: null,
      page_size: 0,
    }
  })
  const [sortingColumn, setSortingColumn] = useState("role")
  const [sortOrder, setSortOrder] = useState<"ASC" | "DESC">("ASC")
  // const [paginationPage, setPaginationPage] = useState(0)
  // const [paginationLimit, setPaginationLimit] = useState(20)
  const [loadingState, setLoadingState] = useState("Loading...")

  const [deleteButtonPressed, setDeleteButtonPressed] = useState(false)
  const [deleteButtonPressedOnUserId, setDeleteButtonPressedOnUserId] = useState(-1)

  let paginationPage = 1
  let paginationPageSize = 5

  // API REQUESTS -------------------------------------------------------------
  // --------------------------------------------------------------------------
  
  // Get all profiles ---------------------------
  useEffect(() => {
    getProfiles()
  }, [sortingColumn, sortOrder])
  let getProfiles = async () => {
    try {
      let response = await api.get((`/shop-api-v1/profiles?offset="0"&page=${paginationPage}&page_size=${paginationPageSize}&sort_by=${sortingColumn}&sort_order=${sortOrder}`))
      // QUESTION how to handle http 400 response message - 'response' value is not accessible in 'catch'
      if (response.status === 200) {
        setTableData(response.data)
        if (response.data.rows.length < 1)
          setLoadingState("Didn't receive any profiles. Nothing to show.")
      }
    } catch (err: any) {
      // console.log("Response: ", err.response)
      console.error("During getting 'Profiles', err occurred: ", err.message, "\nMessage from server:", err.response.data);
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
          rows : prevTableState.rows.filter(row => row.id !== id),
          pagination_description: prevTableState.pagination_description,
        }))
      }
      // QUESTION how to create, that deleted row will disappear animated
    } catch (err: any) {
      console.error("During getting 'Deleting profile', err occurred: ", err.message);
    }
  }


  // FUNCTIONS ----------------------------------------------------------------
  // --------------------------------------------------------------------------


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
                  <span
                    onClick={() => {
                      if (header.sorting) {
                        if (sortingColumn === header.key) {
                          sortOrder === "ASC" ? setSortOrder("DESC") : setSortOrder("ASC");
                        } else {
                          setSortOrder("ASC");
                        }
                        setSortingColumn(header.key)
                      } else {}
                    }}
                    className={`${header.sorting ? "cursor-pointer" : ""}`}
                  >
                    {header.label + String.fromCharCode(160)}
                    {header.sorting && (
                      (sortingColumn === header.key && sortOrder === "ASC" && <span> ▽</span>) ||
                      (sortingColumn === header.key && sortOrder === "DESC" && <span> △</span>) ||
                      (sortingColumn !== header.key && <span> △▽</span>))
                    }
                  </span>
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

      <div
        data-info="numbers-for-pages"
        className="flex justify-center items-center"
      >
        {/* {for (let index = 0; index < array.length; index++) {
          const element = array[index];
          
        }} */}

        Total pages: {tableData.pagination_description.total_pages}
        {/* TODO: page n of m */}
        {/* CONTINUE add pagination */}

      </div>
    </>
  )
}

export default Users