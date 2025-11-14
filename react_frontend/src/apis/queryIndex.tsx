export type ResponseSources = {
    text: string;
    doc_id: string;
    start: number;
    end: number;
    similarity: number;
};

export type QueryResponse = {
    text: string;
    sources: ResponseSources[];
};

const queryIndex = async (query: string): Promise<QueryResponse> => {
    const backendHost = process.env.REACT_APP_BACKEND_HOST;
    const backendPort = process.env.REACT_APP_BACKEND_PORT;
    const queryURL = new URL("http://" + backendHost + ":" + backendPort + "/query?");
    queryURL.searchParams.append("text", query);

    const response = await fetch(queryURL, { mode: "cors" });
    if (!response.ok) {
        return { text: "Error in query", sources: [] };
    }

    const queryResponse = (await response.json()) as QueryResponse;

    return queryResponse;
};

export default queryIndex;
