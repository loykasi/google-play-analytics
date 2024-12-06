import { useState } from "react"
import { makeHttpRequest } from "../helpers/makeHttpRequest"

const useFetch = () => {
    const [loading, setLoading] = useState(false);

    const makeRequest = async (method, endpoint, input) => {
        try {
            setLoading(true)
            const data = await makeHttpRequest(method, endpoint, input);
            return data;
        } catch (error) {
            console.log(error)
        } finally {
            setLoading(false)
        }
    }
    return [loading, makeRequest]
}

export default useFetch