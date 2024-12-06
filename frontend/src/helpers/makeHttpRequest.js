// const baseUrl = "http://database_api:8000"
const baseUrl = "http://127.0.0.1:8000"

export function makeHttpRequest(method, endpoint, input) {
    return new Promise(async (resolve, reject) => {
        try {
            const res = await fetch(`${baseUrl}${endpoint}`, {
                method: method,
                headers: {
                    "content-type": "application/json",
                },
                body: JSON.stringify(input)
            });

            const text = await res.text();
            const data = JSON.parse(text);
            if (!res.ok) {
                reject(data);
            }
            resolve(data);
        } catch (error) {
            console.log('error: ' + error);
            reject(error);
        }
    })
}