# Odisha RERA Projects Scraper

This Python script uses **Selenium** to scrape project data from the [Odisha RERA](https://rera.odisha.gov.in/projects/project-list) portal.

The scraped data is saved in two formats:

- `odisha_projects.html`: A clean HTML table of the extracted data.
- `odisha_projects.txt`: A plain-text file with a table format for easy viewing.

## 🚀 How to Run

1. Clone the repository:

```bash
git clone https://github.com/PrasadHiremath1/web-scrape-assignment.git
cd web-scrape-assignment
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Download and place the correct `chromedriver.exe` in the project directory. Ensure it matches your Chrome version.

4. Run the script:

```bash
python rera_scraper.py
```

> You can remove the `--headless` option from the script if you want to see the browser open during scraping.

## 📦 Requirements

List of Python packages used:

```txt
selenium
```

You can install them using:

```bash
pip install selenium
```

Or simply run:

```bash
pip install -r requirements.txt
```

## 🛠 Notes

- Make sure your `chromedriver` version matches your installed version of Chrome.
- The site may be slow to load. The script includes wait times and checks for dynamic elements to load properly.
