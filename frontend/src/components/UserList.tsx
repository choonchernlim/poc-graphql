"use client";

import { useQuery, gql } from "@apollo/client";

const GET_USERS = gql`
  query GetUsers {
    users {
      id
      name
      accounts {
        id
        name
      }
    }
  }
`;

interface Account {
  id: string;
  name: string;
}

interface User {
  id: string;
  name: string;
  accounts: Account[];
}

interface GetUsersData {
  users: User[];
}

export default function UserList() {
  const { loading, error, data } = useQuery<GetUsersData>(GET_USERS);

  if (loading) return <p className="p-4 text-center">Loading...</p>;
  if (error) return <p className="p-4 text-center text-red-500">Error: {error.message}</p>;

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">Users and Their Accounts</h1>
      <div className="overflow-x-auto">
        <table className="min-w-full bg-white border border-gray-200">
          <thead>
            <tr className="bg-gray-100">
              <th className="py-2 px-4 border-b text-left">User ID</th>
              <th className="py-2 px-4 border-b text-left">User Name</th>
              <th className="py-2 px-4 border-b text-left">Accounts</th>
            </tr>
          </thead>
          <tbody>
            {data?.users.map((user) => (
              <tr key={user.id} className="hover:bg-gray-50">
                <td className="py-2 px-4 border-b">{user.id}</td>
                <td className="py-2 px-4 border-b font-medium">{user.name}</td>
                <td className="py-2 px-4 border-b">
                  <ul className="list-disc list-inside">
                    {user.accounts.map((account) => (
                      <li key={account.id} className="text-sm text-gray-600">
                        {account.name} (ID: {account.id})
                      </li>
                    ))}
                    {user.accounts.length === 0 && (
                      <span className="text-gray-400 italic">No accounts</span>
                    )}
                  </ul>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
