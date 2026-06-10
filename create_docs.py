import os

docs = {
    'van_ness_apartments.txt': 'Van Ness apartments review: The building at Van Ness is close to UDC metro stop. Rent is around 1800 per month for a studio. Management is slow to respond to maintenance requests. Heating works well in winter but AC is unreliable. Good location, walkable to Whole Foods and the metro. Several UDC students live here.',
    'tenleytown_housing.txt': 'Tenleytown area housing review: Living near Tenleytown is convenient for UDC students. The neighborhood is safe and quiet. Rent prices are high, averaging 2000 plus for a one bedroom. Landlords are generally responsive. Public transit is excellent with the red line nearby.',
    'reddit_udc_housing_1.txt': 'Reddit post from UDC student: I lived off campus for two years near Van Ness. Biggest issues were parking and package theft in the lobby. The upside is being so close to campus. Would recommend looking at buildings on Albemarle Street for better value.',
    'reddit_udc_housing_2.txt': 'Reddit thread about UDC off campus: Many students said the on campus housing lottery is unpredictable so they looked off campus. Suggestions included checking Facebook groups for sublets and avoiding certain buildings on Connecticut Ave due to mold reports.',
    'google_review_van_ness_1.txt': 'Google review of Van Ness apartment complex: Three stars. The location is great for UDC students, literally a 5 minute walk to campus. However the management company is unresponsive and it took three months to fix a broken elevator. Noise from Connecticut Ave can be loud at night.',
    'google_review_tenleytown_1.txt': 'Google review of Tenleytown housing: Four stars. Clean building, responsive super, safe neighborhood. A bit pricey but worth it for the safety and proximity to UDC. Several grad students live here. Laundry in building is a plus.',
    'housing_tips_udc.txt': 'UDC student housing tips shared on Discord: Start looking for housing in February for fall semester. Most good apartments near campus get taken fast. Budget at least 1500 per month for a studio. Avoid month to month leases as they cost more. Check if utilities are included before signing.',
    'connecticut_ave_review.txt': 'Review of Connecticut Avenue apartments near UDC: Mixed experiences reported by students. Some buildings have roach problems especially in older units. Newer buildings around 4000 block are better maintained. Price range 1600 to 2200 for studios. Metro access is excellent.',
    'albemarle_street_housing.txt': 'Student review of Albemarle Street housing options: Good value compared to Connecticut Ave. Quieter street, mostly residential. A few buildings allow short term leases which is good for grad students. Some units are older and need renovation. Average rent around 1500 for a studio.',
    'udc_housing_facebook_group.txt': 'Facebook group posts about UDC off campus housing: Students warn about a landlord on Nebraska Ave who keeps security deposits unfairly. Recommendations to always do a walkthrough checklist and document everything before moving in. Best months to find deals are December and January when fewer students are looking.'
}

for filename, content in docs.items():
    filepath = os.path.join('documents', filename)
    with open(filepath, 'w') as f:
        f.write(content)
    print(f'Created {filename}')

print('Done! All 10 documents created.')