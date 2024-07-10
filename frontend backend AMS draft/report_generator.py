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



# html_content = """
# <!DOCTYPE html>
# <html lang="en">
# <head>
#     <meta charset="UTF-8">
#     <meta name="viewport" content="width=device-width, initial-scale=1.0">
#     <title>Apartment Management System Report</title>
#     <style>
#         body {
#             font-family: Arial, sans-serif;
#             margin: 1cm;
#         }
#         h1 {
#             text-align: center;
#         }
#         p {
#             text-align: center;
#         }
#         table {
#             width: 100%;
#             border-collapse: collapse;
#             margin-top: 20px;
#             page-break-inside: auto;
#         }
#         th, td {
#             border: 1px solid #ddd;
#             padding: 8px;
#             text-align: left;
#             page-break-inside: avoid;
#             page-break-after: auto;
#         }
#         th {
#             background-color: #f2f2f2;
#         }
#         .page {
#             page-break-after: always;
#         }
#         .last-page {
#             page-break-after: auto;
#         }
#     </style>
# </head>
# <body>
#     <!-- Title Page -->
#     <div class="page">
#         <h1>Apartment Management System Report</h1>
#         <p>{report_date}</p>
#     </div>
#
#     <!-- Financial Summary Report -->
#     <div class="page">
#         <h1>Financial Summary Report</h1>
#         <table>
#             <thead>
#                 <tr>
#                     <th>Rent Collection</th>
#                     <th>Expenses</th>
#                 </tr>
#             </thead>
#             <tbody>
#                 {financial_table_rows}
#             </tbody>
#         </table>
#         <p>Total Revenue: {total_revenue}</p>
#         <p>Total Expenses: {total_expenses}</p>
#         <p>Net Income: {net_income}</p>
#     </div>
#
#     <!-- Occupancy Rate Report -->
#     <div class="page">
#         <h1>Occupancy Rate Report</h1>
#         <table>
#             <thead>
#                 <tr>
#                     <th>Building Name</th>
#                     <th>Unit Number</th>
#                     <th>Rental Rates</th>
#                 </tr>
#             </thead>
#             <tbody>
#                 {occupancy_table_rows}
#             </tbody>
#         </table>
#         <p>Occupancy Rate: {occupancy_rate}</p>
#         <p>Average Rental Rate: {average_rental_rate}</p>
#     </div>
#
#     <!-- Tenant Demographic Report -->
# <div class="last-page">
#     <h1>Tenant Demographic Report</h1>
#     <table>
#         <thead>
#             <tr>
#                 <th>Tenant Name</th>
#                 <th>Age</th>
#                 <th>Gender</th>
#                 <th>Income</th>
#             </tr>
#         </thead>
#         <tbody>
#             <tr>
#                 <td>Age 18-24</td>
#                 <td>{age_18_24}</td>
#             </tr>
#             <tr>
#                 <td>Age 25-34</td>
#                 <td>{age_25_34}</td>
#             </tr>
#             <tr>
#                 <td>Age 35-44</td>
#                 <td>{age_35_44}</td>
#             </tr>
#             <tr>
#                 <td>Age 45-54</td>
#                 <td>{age_45_54}</td>
#             </tr>
#             <tr>
#                 <td>Age 55+</td>
#                 <td>{age_55_plus}</td>
#             </tr>
#             <tr>
#                 <td>Male Count</td>
#                 <td>{male_count}</td>
#             </tr>
#             <tr>
#                 <td>Female Count</td>
#                 <td>{female_count}</td>
#             </tr>
#             <tr>
#                 <td>Preferred Not to Say Count</td>
#                 <td>{preferred_not_to_say_count}</td>
#             </tr>
#             <tr>
#                 <td>Income &lt; 20000</td>
#                 <td>{income_lt_20000}</td>
#             </tr>
#             <tr>
#                 <td>Income 20000-40000</td>
#                 <td>{income_20000_40000}</td>
#             </tr>
#             <tr>
#                 <td>Income 40000-60000</td>
#                 <td>{income_40000_60000}</td>
#             </tr>
#             <tr>
#                 <td>Income &gt; 60000</td>
#                 <td>{income_gt_60000}</td>
#             </tr>
#         </tbody>
#     </table>
#     <p>Age Distribution: {age_distribution}</p>
#     <p>Gender Distribution: {gender_distribution}</p>
#     <p>Income Range: {income_range}</p>
# </div>
# </body>
# </html>
# """
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

