# poc-graphql Frontend

A modern Next.js application built with TypeScript and Tailwind CSS, demonstrating how to integrate **Apollo Client** to consume a GraphQL API.

## Description

This frontend provides a clean, responsive interface to view users and their associated accounts. It is designed to work seamlessly with the FastAPI/Strawberry backend located in the `backend/` directory.

### Key Features
- **Apollo Client Integration**: Configured with a dedicated wrapper to provide GraphQL capabilities across the app.
- **Dynamic Data Fetching**: Uses the `useQuery` hook to fetch and display real-time data from the backend.
- **Tailwind CSS Styling**: A polished, table-based UI for clear data presentation.
- **TypeScript Powered**: Fully typed interfaces for GraphQL responses, ensuring type safety and better developer experience.

---

## Getting Started

### Prerequisites
- **Node.js**: Version 18.x or later.
- **Backend**: Ensure the [FastAPI backend](../backend/README.md) is running at `http://localhost:8000/graphql`.

### 1. Installation
Navigate to this directory and install the dependencies:
```bash
cd frontend
npm install
```

### 2. Run the Development Server
Start the Next.js development server:
```bash
npm run dev
```

### 3. View the App
Open [http://localhost:3000](http://localhost:3000) in your browser to see the result.

---

## Project Structure

- `src/app/`: Next.js App Router pages and layouts.
- `src/components/`: Reusable React components (e.g., `UserList.tsx`).
- `src/lib/`: Library configurations, including `apollo-wrapper.tsx`.

## Learn More

- [Next.js Documentation](https://nextjs.org/docs)
- [Apollo Client Docs](https://www.apollographql.com/docs/react/)
- [Tailwind CSS Docs](https://tailwindcss.com/docs)
