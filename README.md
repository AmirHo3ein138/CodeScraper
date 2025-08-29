### CodeScraper – Group Project

This project was developed as a **group project** in collaboration with my classmates.  
It is a **web scraping and machine learning tool** that collects villa advertisement data from **two well-known real estate websites** and compares them to detect duplicate listings and find the best deals.  

Key Features:
- **Data Collection:** Scrapes detailed information such as price, location, owner contact, and other attributes from both websites.  
- **Data Processing:** Cleans and organizes the collected data for analysis.  
- **Data Storage:** Stores the collected data into a database using **SQL commands**.  
- **Duplicate Detection:** Uses **machine learning algorithms (Scikit-learn)** to identify listings that are actually the same villa appearing on both sites.  
- **Price Comparison:** Highlights the best option by comparing prices of similar or duplicate listings.  
- **Final Output:** Exports the final processed results into a clean and well-structured **Excel file** for easy review.  

Technologies & Libraries:
- **Selenium** – For automated browser-based scraping.  
- **BeautifulSoup (bs4)** – For parsing and extracting HTML data.  
- **Requests** – For making HTTP requests.  
- **SQL** – For structured data storage.  
- **Scikit-learn** – For applying ML algorithms to detect similarities between ads.  
- **Excel Export (pandas / openpyxl)** – For generating the final report.  

Outcome:
- Provides a consolidated dataset of villa listings.  
- Helps users **identify duplicate ads** across different sites.  
- Assists in selecting the **best deal at the best price**, with results stored in **SQL** and exported to a professional **Excel report**.  
