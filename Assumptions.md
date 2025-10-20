## Assumptions
- Input File Robustness: We make no assumptions about the validity of user input files; the code is designed to handle various types of invalid or malformed input.

- Stock Availability: We do not assume that all stocks provided by the user will be available in the pricing data files.

- Configurable Holdings: The underlying code supports configuration of the number of top holdings, but this feature is not currently enabled for the user.

- Internal Reporting: Since this tool is for internal organizational use, we will implement verbose error reporting to inform users specifically about input file issues.

- Data Persistence: We assume there is no current requirement to persistently store user input files.

- System Simplicity: Given the current small data size, we assume no need to separate APIs, prioritizing a simpler system architecture.

- Maintainability: The project requires monitoring and logging capabilities to support future maintenance and debugging.

- In-Memory Data: Based on current data showing that ETF holdings do not exceed 1000 stocks, we assume the data size is small enough to be loaded entirely into memory, eliminating the need for databases or caching systems.

- Pricing File Integrity: We assume the pricing data files are well-formatted and do not require extensive validation.

- Future Scalability (Pricing): We assume we will not encounter larger pricing.csv files in the future that would necessitate a new API endpoint for ETF price time series (e.g., one implementing frontend-requested range filtering and server-side downsampling).