import asyncio
from playwright.async_api import async_playwright

html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tenant Information Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; }}
        h1 {{ text-align: center; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background-color: #f2f2f2; }}
    </style>
</head>
<body>
    <h1>Tenant Information Report</h1>
    <p>This report summarizes tenant information and their payment status.</p>
    <table>
        <thead>
            <tr>
                <th>Building Name</th>
                <th>Unit Number</th>
                <th>Tenant Name</th>
                <th>Contact Number</th>
                <th>Payment Status</th>
                <th>Lease Start Date</th>
            </tr>
        </thead>
        <tbody>
            {table_rows}
        </tbody>
    </table>
</body>
</html>
"""

def generate_table_rows(tenant_data):
    rows = ""
    for tenant in tenant_data:
        rows += f"""
        <tr>
            <td>{tenant['building_name']}</td>
            <td>{tenant['unit_number']}</td>
            <td>{tenant['tenant_name']}</td>
            <td>{tenant['contact_number']}</td>
            <td>{tenant['payment_status']}</td>
            <td>{tenant['lease_start_date']}</td>
        </tr>
        """
    return rows

async def create_pdf_report(tenant_data, output_filename):
    table_rows = generate_table_rows(tenant_data)
    html_content_with_data = html_content.format(table_rows=table_rows)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)  # Launch in non-headless mode
        page = await browser.new_page()
        await page.set_content(html_content_with_data)
        await page.pdf(path=output_filename)

        # Display an alert to inform the user to close the browser manually
        await page.evaluate('alert("PDF generated successfully. Please close the browser manually.")')

        # Keep the script running indefinitely
        await asyncio.Future()

# async def create_pdf_report(conn, start_date, end_date, output_filename):
#     financial_summary = generate_financial_summary(conn, start_date, end_date)
#     occupancy_rate = generate_occupancy_rate(conn)
#     tenant_demographic = generate_tenant_demographic(conn)
#
#     # Format the data into an HTML template and generate the PDF
#     html_content_with_data = html_content.format(
#         total_income=financial_summary['total_income'],
#         total_expense=financial_summary['total_expense'],
#         net_income=financial_summary['net_income'],
#         occupancy_rate=occupancy_rate['occupancy_rate'],
#         average_rent=occupancy_rate['average_rent'],
#         total_units=occupancy_rate['total_units'],
#         age_distribution=tenant_demographic['age_distribution'],
#         gender_distribution=tenant_demographic['gender_distribution'],
#         occupation_distribution=tenant_demographic['occupation_distribution'],
#         income_range_distribution=tenant_demographic['income_range_distribution']
#     )
#
#     async with async_playwright() as p:
#         browser = await p.chromium.launch(headless=False)  # Launch in non-headless mode
#         page = await browser.new_page()
#         await page.set_content(html_content_with_data)
#         await page.pdf(path=output_filename)
#
#         # Display an alert to inform the user to close the browser manually
#         await page.evaluate('alert("PDF generated successfully. Please close the browser manually.")')
#
#         # Keep the script running indefinitely
#         await asyncio.Future()

