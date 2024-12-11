export async function retryWithExponentialBackoff(apiCall, maxRetries = 5, initialDelay = 500) {
    let retries = 0;
    let delay = initialDelay;

    while (retries < maxRetries) {
        try {
            // Attempt the API call
            return await apiCall();
        } catch (error) {
            if (retries === maxRetries - 1) {
                throw error;
            }
            // Retry only for network failures or server errors
            if (!error.response || [500, 503].includes(error.response.status)) {
                console.warn(`Retrying API request... Attempt ${retries + 1}`);
                retries++;

                // Wait for the delay time
                await new Promise((resolve) => setTimeout(resolve, delay));

                // Increase delay exponentially
                delay *= 2;
            }
        }
    }
}
