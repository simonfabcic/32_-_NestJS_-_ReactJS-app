import { useEffect, useState } from "react";
import useAxios from "../../utils/useAxios";
import { useNavigate } from "react-router-dom";

const Users = () => {
  interface Header {
    key: string;
    label: string;
    sorting: boolean;
  }

  interface Row {
    avatar: string;
    id: number;
    email: string;
    full_name: string;
    role: string;
  }

  interface ApiResponseProfiles {
    headers: Header[];
    rows: Row[];
    pagination_description: {
      current_page: number;
      total_pages: number;
      sort_order: "ASC" | "DESC";
      sort_by: string;
      total_records: number;
      prev_page: number | null;
      next_page: number | null;
      page_size: number;
    };
  }

  const baseURL = import.meta.env.VITE_BACKEND_BASE_URL;
  let api = useAxios();
  const navigate = useNavigate();
  const paginationPageSize = 100;

  const [tableData, setTableData] = useState<ApiResponseProfiles>({
    headers: [],
    rows: [],
    pagination_description: {
      current_page: 0,
      total_pages: 0,
      sort_order: "ASC",
      sort_by: "",
      total_records: 0,
      prev_page: null,
      next_page: null,
      page_size: 0,
    },
  });
  const [sortingColumn, setSortingColumn] = useState("role");
  const [sortOrder, setSortOrder] = useState<"ASC" | "DESC">("ASC");
  const [loadingState, setLoadingState] = useState("Loading...");
  const [deleteButtonPressed, setDeleteButtonPressed] = useState(false);
  const [deleteButtonPressedOnUserId, setDeleteButtonPressedOnUserId] = useState(-1);
  const [paginationWantedPage, setPaginationWantedPage] = useState(1);
  const [paginationPageNumbers, setPaginationPageNumbers] = useState<number[]>([]);

  const AvatarCell: React.FC<{avatar_image_src_url:string}> = ({avatar_image_src_url}) => {
    return (
      <td className="h-full">
        {avatar_image_src_url === null
        ? "/"
        : <img src={baseURL+avatar_image_src_url} className="h-8 rounded-lg block mx-auto" alt="avatar" />}
      </td>
    )
  }  
  const TextCell: React.FC<{text:string | number}> = ({text}) => {
    return (
      <td>
        {text}
      </td>
    )
  }

  // Get all profiles
  useEffect(() => {
    getProfiles();
  }, [sortingColumn, sortOrder, paginationWantedPage]);
  let getProfiles = async () => {
    try {
      let response = await api.get(
        `/shop-api-v1/profiles?offset=0&page=${paginationWantedPage}&page_size=${paginationPageSize}&sort_by=${sortingColumn}&sort_order=${sortOrder}`,
      );
      if (response.status === 200) {
        setTableData(() => response.data);
        if (response.data.rows.length < 1)
          setLoadingState("Didn't receive any profiles. Nothing to show.");
        let currentPage = response.data.pagination_description.current_page;
        let startPage = Math.max(1, currentPage - 2);
        let endPage = Math.min(
          currentPage + 2,
          response.data.pagination_description.total_pages,
        );
        let newNumbers: number[] = [];
        for (let i = startPage; i <= endPage; i++) newNumbers.push(i);
        setPaginationPageNumbers(newNumbers);
      }
    } catch (err: any) {
      console.error(
        "During getting 'Profiles', err occurred: ",
        err.message,
        "\nMessage from server:",
        err?.response?.data,
      );
      setLoadingState("Can't get profiles data. Contact admin...");
    }
  };

  // Delete profile
  let deleteProfile = async (id: number) => {
    try {
      let response = await api.delete(`/shop-api-v1/profile/${id}`);
      if (response.status === 204) {
        setTableData((prevTableState) => ({
          headers: prevTableState.headers,
          rows: prevTableState.rows.filter((row) => row.id !== id),
          pagination_description: prevTableState.pagination_description,
        }));
      }
      // QUESTION how to create, that deleted row will disappear animated
    } catch (err: any) {
      console.error(
        "During getting 'Deleting profile', err occurred: ",
        err.message,
      );
    }
  };

  return (
    <>
      <div>Users</div>
      <button
        className="px-4 py-2 bg-gray-400 rounded-md"
        onClick={() => navigate("add-new")}
      >
        Add User
      </button>
      {tableData.headers.length > 0 && tableData.rows.length > 0 ? (
        <table className="w-full text-center">
          <thead>
            <tr>
              <th>No.</th>
              {tableData.headers &&
                tableData.headers.map((header) => (
                  <th key={header.label}>
                    <span
                      onClick={() => {
                        if (header.sorting) {
                          if (sortingColumn === header.key) {
                            sortOrder === "ASC"
                              ? setSortOrder("DESC")
                              : setSortOrder("ASC");
                          } else {
                            setSortOrder("ASC");
                          }
                          setSortingColumn(header.key);
                        } else {
                        }
                      }}
                      className={`${header.sorting ? "cursor-pointer" : ""}`}
                    >
                      {header.label + String.fromCharCode(160)}
                      {header.sorting &&
                        ((sortingColumn === header.key &&
                          sortOrder === "ASC" && <span> ▽</span>) ||
                          (sortingColumn === header.key &&
                            sortOrder === "DESC" && <span> △</span>) ||
                          (sortingColumn !== header.key && <span> △▽</span>))}
                    </span>
                  </th>
                ))}
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {tableData.rows &&
              tableData.rows.map((row, index) => (
                <tr
                  key={row.id}
                  className={`
                  h-14
                  ${
                    deleteButtonPressed && deleteButtonPressedOnUserId == row.id
                      ? "bg-red-200"
                      : "even:bg-gray-400"
                  }
                `}
                >
                  <td>
                    {index +
                      1 +
                      (paginationWantedPage - 1) * paginationPageSize}
                  </td>
                  {tableData.headers.map((header) => (
                    header.key === "avatar"
                    ? <AvatarCell key={header.key} avatar_image_src_url={row[header.key]} />
                    : <TextCell key={header.key} text={row[header.key as keyof Row]} />
                  ))}
                  <td className="space-x-2">
                    <button
                      className="w-10 h-8 bg-yellow-300 rounded"
                      onClick={() => navigate(`${row.id}`)}
                    >
                      Edit
                    </button>
                    <button
                      className="bg-red-500 hover:bg-red-600 text-white py-1 px-3 rounded"
                      onClick={() => {
                        deleteProfile(row.id);
                        setDeleteButtonPressedOnUserId(row.id);
                      }}
                      onMouseDown={() => {
                        setDeleteButtonPressed(true);
                        setDeleteButtonPressedOnUserId(row.id);
                      }}
                      onMouseUp={() => {
                        setDeleteButtonPressed(false);
                        setDeleteButtonPressedOnUserId(-1);
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
      ) : (
        <p className="font-bold">{loadingState}</p>
      )}

      {tableData.rows.length > 0 && (
        <div
          data-info="numbers-for-pages"
          className="flex justify-center items-center gap-1 mt-3 mb-3"
        >
          {!paginationPageNumbers.includes(1) && (
            <>
              <button
                onClick={() => setPaginationWantedPage(1)}
                className="w-10 h-8 bg-gray-400 rounded-md mr-2"
              >
                {"1..."}
              </button>
            </>
          )}
          {paginationPageNumbers.map((pageNumber) => (
            <button
              key={pageNumber}
              onClick={() => setPaginationWantedPage(pageNumber)}
              className={`${
                pageNumber === paginationWantedPage
                  ? "font-bold cursor-default"
                  : ""
              } w-10 h-8 bg-gray-400 rounded-md`}
            >
              {pageNumber}
            </button>
          ))}
          {!paginationPageNumbers.includes(
            tableData.pagination_description.total_pages,
          ) && (
            <>
              <button
                onClick={() =>
                  setPaginationWantedPage(
                    tableData.pagination_description.total_pages,
                  )
                }
                className="w-10 h-8 bg-gray-400 rounded-md ml-2"
              >
                {"..." + tableData.pagination_description.total_pages}
              </button>
            </>
          )}
        </div>
      )}
    </>
  );
};

export default Users;
