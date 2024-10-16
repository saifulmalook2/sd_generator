from openai import AsyncAzureOpenAI
import os
import json
from scrape import scrape_main, parse_pdf, parse_pdf_page, parse_vendors



client = AsyncAzureOpenAI(
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version="2024-02-15-preview",
    azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
)

async def dc_1(company_name, url):

    url = f"https://{url}"
    company_info = await scrape_main(url)

    try:
        response = await client.chat.completions.create(
            # response_format={"type": "json_object"},
            model="gpt-4o",
            temperature = 0.3,
            messages=[
            {"role": "system", "content": "You are an assistant that strictly provides answers based only on the provided content. Do not speculate, hallucinate, or provide information not directly found in the content."},
            {
                    "role": "user",
                    "content": (
                        f"Review the given content and write a 2-3 paragraphs regarding the 'Company overview and types of products and services provided' for {company_name} "
                        f"The entire information should be strictly based on the following: {company_info}"
                    )
                }            
                ],
            
        )

        response_text = response.choices[0].message.content.strip()
        paragraphs = response_text.split("\n\n")
        heading = "DC 1: Company Overview and Types of Products and Services Provided"
        return {"heading" : heading, "paragraphs" : paragraphs, "points" : [], "table" : None}

    except Exception as e:
        print("Error", e)
        heading = "DC 1: Company Overview and Types of Products and Services Provided"
        return {"heading" : heading, "paragraphs" : [], "points" : [], "table" : None}

def dc_2(company_name, type):

    # NEED ACTUAL POINTS
    template_texts = {
        "SOC 2 Type I: Security" : [
                "System features and configuration settings designed to authorize user access while restricting unauthorized users from accessing information not needed for their role",
                "Regular vulnerability scans over the system and network, and penetration tests over the production environment",
                "Operational procedures for managing security incidents and breaches, including notification procedures",
                "Use of encryption technologies to protect customer data both at rest and in transit",
                "Use of data retention and data disposal",
                "Uptime availability of production systems"
                ],
    }

    dc_2_main = f'''{company_name} designs its processes and procedures related to the system to meet its objectives. Those objectives are based on the service commitments that {company_name} makes to user entities, the laws, and regulations that govern the provision of the services, and the financial, operational, and compliance requirements that {company_name} has established for the services. The system services are subject to the Security commitments established internally for its services.\n\n
                    {company_name}'s commitments to users are communicated through Service Level Agreements, Master Services Agreements, Statements of Work, Work Orders, Online Privacy Policy and Terms of Use. \n\n
                    Security commitments include, but are not limited to, the following: 
                    '''

    heading = "DC 2: Principal service commitments and system requirements"

    response = {
        "heading" : heading,
        "paragraphs" : dc_2_main.split("\n\n"),
        "points" : template_texts[type], 
        "table" : None

    }
    return response

def dc_3():

    dc_3_points =  ['''Software - The application programs and IT system software that supports
                    application programs (operating systems, middleware, and utilities), the
                    types of databases used, the nature of external facing web applications,
                    and the nature of applications developed in-house, including details
                    about whether the applications in use are mobile applications or desktop
                    or laptop applications.''',
                    '''People - The personnel involved in the governance, operation, security,
                    and use of a system (business unit personnel, developers, operators, user
                    entity personnel, vendor personnel, and managers).
                    ''',
                    '''Data - The types of data used by the system, such as transaction streams,
                    files, databases, tables, and output used or processed by the system
                    ''',
                    '''Procedures - The automated and manual procedures related to the
                    services provided, including, as appropriate, procedures by which service
                    activities are initiated, authorized, performed, and delivered, and reports
                    and other information prepared.

                    '''
                    ]

    dc_3_main = f'''The System description is comprised of the following components:\n\n'''

    heading = "DC 3 : Components of the System"

    response = {
        "heading" : heading,
        "paragraphs" : dc_3_main.split("\n\n"),
        "points" : dc_3_points,
        "table" : None

    }
    return response

def dc_3_1(company_name):
    dc_3_main = f'''{company_name} maintains a system inventory that includes virtual machines,
                    computers (desktops and laptops), and networking devices (switches and
                    routers). The inventory documents device name, inventory type, description,
                    and owner. To outline the topology of its network, the organization maintains the
                    following network diagram(s):\n\nPlease complete this section...'''

    heading = "3.1 Infrastructure"

    response = {
        "heading" : heading,
        "paragraphs" : dc_3_main.split("\n\n"),
        "points" : [], 
        "table" : None
    }
    return response

async def dc_3_2(company_name, system):
    dc_3_main = f'''{company_name} is responsible for managing the development and operation
                of the {system} system including infrastructure components such as
                servers, databases, and storage systems. The in-scope {company_name}.
                infrastructure and software components are shown in the table provided below:'''

    heading = "3.2 : Software"

    vendors = parse_vendors(f"uploads/{company_name}_vendors.xlsx")
    try:
        response = await client.chat.completions.create(
            response_format={"type": "json_object"},
            model="gpt-4o",
            temperature = 0.3,
            messages=[
            {"role": "system", "content": "You are an assistant that strictly provides answers based only on the provided content. Do not speculate, hallucinate, or provide information not directly found in the content."},
            {
                    "role": "user",
                    "content": (
                        f"Review the given list of company's and their respective website and write a 1 line (3-6 words) description of what the respective comany's purpose is, and what Operating System it uses. Return a JSON like this 'vendors' : [{{'name' : 'AWS', 'os' : 'AWS', 'purpose' :'Cloud Hosting' }},...]"
                        f"If the company does not have a website listed you can skip leave the 'os' and 'purpose' empty "
                        f"The entire information should be strictly based on the following: {vendors}"
                    )
                }            
                ],
            
        )

        response_text = response.choices[0].message.content.strip()
        vendor_details = json.loads(response_text)

        names = [item.get('name') for item in vendor_details["vendors"]]
        os_list = [item.get('os') for item in vendor_details["vendors"]]
        purposes = [item.get('purpose') for item in vendor_details["vendors"]]
        
        table_data = {"System/Aplication" : names, "Operating System" : os_list, "Purpose" : purposes}
        
        response = {
        "heading" : heading,
        "paragraphs" : dc_3_main.split("\n\n"),
        "points" : [], 
        "table" : table_data
        }
        return response

    except Exception as e:
        print("Error", e)
        return {"heading" : heading, "paragraphs" : [], "points" : [], "table" : None}

def dc_3_3():
    dc_3__3main = f'''The company employs dedicated team members to handle major product functions, including operations, and support. 
    The IT/Engineering Team monitors the environment, as well as manages data backups and recovery. The Company focuses on hiring the right people for the right job as well as 
    training them both on their specific tasks and on the ways to keep the company and its data secure:\n\nPlease complete this section...'''

    heading = "3.3 People"

    response = {
        "heading" : heading,
        "paragraphs" : dc_3__3main.split("\n\n"),
        "points" : [], 
        "table" : None
    }
    return response
    
async def dc_3_4(company_name):

    data_policy_text = parse_pdf(f"uploads/{company_name}_data_policy.pdf")


    template_js = {
    "Category": [
        "..."
    ],
    "Description": [
        "..."
        ],
    "Examples": [
       ["...", "..."],
       ]

    }
    try:
        response = await client.chat.completions.create(
            response_format={"type": "json_object"},
            model="gpt-4o",
            temperature = 0.3,
            messages=[
            {"role": "system", "content": "You are an assistant that strictly provides answers based only on the provided content. Do not speculate, hallucinate, or provide information not directly found in the content."},
            {
                    "role": "user",
                    "content": (
                        f"Review the given content and classify the DATA used by the company into different categories, for each category get the description (1-2 sentences), and for each category get the examples and summarize them. {company_name} "
                        f"Return a JSON after the data is extracted the JSON should be of the following format : {template_js}"
                        f"The entire information should be strictly based on the following: {data_policy_text}"
                    )
                }            
                ],
            
        )

        response_text = response.choices[0].message.content.strip()

        table_data = json.loads(response_text)

    except Exception as e:
        print("Error", e)
        return {"heading" : heading, "paragraphs" : [], "points" : [], "table" : None}



    dc_3_4_main = f'''Data as defined by {company_name}, constitutes the following:\n\n

                    User and account data - this includes Personally Identifiable Information (PII) and other data from employees, customers,
                    users (customers' employees), and other third parties such as suppliers, vendors, business partners, and contractors. 
                    This collection is permitted under the Terms of Use and Privacy Policy (as well as other separate agreements with vendors, 
                    partners, suppliers, and other relevant third parties). Access to PII is controlled through processes for provisioning system
                    permissions, as well as ongoing monitoring activities, to ensure that sensitive data is restricted to employees based on job function.\n\n

                    Data is categorized in the following major types of data used by {company_name}\n\n
                '''

    heading = "3.4 Data"


    response = {
        "heading" : heading,
        "paragraphs" : dc_3_4_main.split("\n\n"),
        "points" : [], 
        "table" : table_data
    }
    return response

def dc_3_4_ending(company_name):
    dc_3_main = f'''Customer data is managed, processed, and stored in accordance with the relevant data protection and other
                 regulations, with specific requirements formally established in customer agreements, if any. Customer data is captured 
                 which is utilized by the company in delivering its services.\n\n
                All personnel and contractors of the company are obligated to respect and, in all cases, to protect customer data. Additionally, {company_name} has policies and procedures in place to ensure proper and secure handling of customer data. These policies 
                and procedures are reviewed on at least an annual basis.
                '''

    heading = None

    response = {
        "heading" : heading,
        "paragraphs" : dc_3_main.split("\n\n"),
        "points" : [], 
        "table" : None
    }
    return response

async def dc_3_5(company_name):

    procedure_policy_text = parse_pdf_page(f"uploads/{company_name}_policy_packet.pdf", 1)
    heading = "3.5 Processes and Procedures"

    try:
        response = await client.chat.completions.create(
            response_format={"type": "json_object"},
            model="gpt-4o",
            temperature = 0.3,
            messages=[
            {"role": "system", "content": "You are an assistant that strictly provides answers based only on the provided content. Do not speculate, hallucinate, or provide information not directly found in the content."},
            {
                    "role": "user",
                    "content": (
                        f"Review the given content and return the Table of Contents as a list keeping the wording as it is, ignore the page number. Just list down all the policies mentioned."
                        f"Return a JSON after the data is extracted the JSON should be of the following format : '{{'contents' : ['...', '...']}}'"
                        f"This is the table of contents: {procedure_policy_text}"
                    )
                }            
                ],
            
        )

        response_text = response.choices[0].message.content.strip()

        contents = json.loads(response_text)
        points_data = contents["contents"]

    except Exception as e:
        print("Error", e)
        return {"heading" : heading, "paragraphs" : [], "points" : [], "table" : None}



    dc_3_4_main = f'''Management has developed and communicated policies and procedures to manage the information security of the system. 
                        Changes to these procedures are performed annually and authorized by management, 
                        the executive team, and control owners. These procedures cover the following key security life cycle areas:\n\n
                '''



    response = {
        "heading" : heading,
        "paragraphs" : dc_3_4_main.split("\n\n"),
        "points" : points_data, 
        "table" : None
    }
    return response

def dc_3_5_1(company_name, provider):
    dc_3_main = f'''{company_name}'s production servers are maintained by {provider}. The physical and environmental security 
                    protections are the responsibility of {provider}. {company_name} reviews the attestation reports and performs a 
                    risk analysis of {provider} on at least an annual basis.
                    '''

    heading = "3.5.1 Physical Security"

    response = {
        "heading" : heading,
        "paragraphs" : dc_3_main.split("\n\n"),
        "points" : [], 
        "table" : None
    }
    return response

def dc_3_5_2(company_name, hire_days, revoke_days):
    dc_3_main = f'''{company_name} provides employees and contracts access to infrastructure via a role-based access control system, to ensure 
    uniform, least privilege access to identified users and to maintain simple and reportable user provisioning and deprovisioning 
    processes.\n\n
    Access to these systems is split into admin roles, user roles, and no access roles. User access and roles are reviewed on an annual
    basis to ensure least privilege access.\n\n
    The Engineering Team is responsible for provision access to the system based on the employee's role and performing a background check. 
    The employee is responsible for reviewing {company_name}'s policies, completing security training. These steps must be completed within {hire_days} days of 
    hire.\n\n
    When an employee is terminated, the Engineering Team is responsible for deprovisioning access to all in scope systems within {revoke_days} days for 
    that employee's termination.\n\n
    '''

    heading = "3.5.2 Logical Access"

    response = {
        "heading" : heading,
        "paragraphs" : dc_3_main.split("\n\n"),
        "points" : [], 
        "table" : None
    }
    return response

def dc_3_5_3(provider):
    dc_3_main = f'''Customer data is backed up and monitored by the Engineering Team for completion and exceptions. If there is an 
    exception, the Engineering Team will perform troubleshooting to identify the root cause and either rerun the backup or as part of 
    the next scheduled backup job.\n\n
    Backup infrastructure is maintained in {provider} with physical access restricted according to the policies. Backups are
    encrypted, with access restricted to key personnel.
    '''

    heading = "3.5.3 Computer Operations - Backups"

    response = {
        "heading" : heading,
        "paragraphs" : dc_3_main.split("\n\n"),
        "points" : [], 
        "table" : None
    }
    return response

def dc_3_5_4(company_name):
    dc_3_main = f'''{company_name} maintains an incident response plan to guide employees on reporting and responding to any information security 
    or data privacy events or incidents. Procedures are in place for identifying, reporting and acting upon breaches or other incidents.\n\n
    {company_name} internally monitors all applications, including the web UI, databases, and cloud storage to ensure that service delivery matches SLA 
    requirements.\n\n
    {company_name} utilizes vulnerability scanning software that checks source code for common security issues as well as for vulnerabilities 
    identified in open-source dependencies and maintains an internal SLA for responding to those issues.\n\n

    '''

    heading = "3.5.4 Computer Operations - Availability"

    response = {
        "heading" : heading,
        "paragraphs" : dc_3_main.split("\n\n"),
        "points" : [], 
        "table" : None
    }
    return response

def dc_3_5_5(company_name):

    dc_3_main = f'''{company_name} maintains documented Systems Development Life Cycle (SDLC) policies and procedures to guide personnel 
    in documenting and implementing application and infrastructure changes. Change control procedures include change request and 
    initiation processes, documentation requirements, development practices, quality assurance testing requirements, and required 
    approval procedures.\n\n
    A ticketing system is utilized to document the change control procedures for changes in the application and implementation of new changes.
    Quality assurance testing and User Acceptance Testing (UAT) results are documented and maintained with the associated change request. 
    Development and testing are performed in an environment that is logically separated from the production environment. Management approves 
    changes prior to migration to the production environment and documents those approvals within the ticketing system.\n\n
    Version control software is utilized to maintain source code versions and migrate source code through the development process to the 
    production environment. The version control software maintains a history of code changes to support rollback capabilities and tracks 
    changes to developers.\n\n
    '''

    heading = "3.5.5 Change Control"

    response = {
        "heading" : heading,
        "paragraphs" : dc_3_main.split("\n\n"),
        "points" : [], 
        "table" : None
    }
    return response

def dc_3_5_6(company_name):
    dc_3_main = f'''{company_name} has elected to use a platform-as-a-service (PaaS) to run its production infrastructure in part to avoid the 
    complexity of network monitoring, configuration, and operations. The PaaS simplifies our logical network configuration by providing 
    an effective firewall around all the {company_name} application containers, with the only ingress from the network via HTTPS connections to 
    designated web frontend endpoints.\n\n
    The PaaS provider also automates the provisioning and deprovisioning of containers to match the desired configuration; if an application 
    container fails, it will be automatically replaced, regardless of whether that failure is in the application or on underlying hardware.\n\n
    {company_name} Inc engages an external firm to perform annual penetration testing to look for unidentified vulnerabilities, and the product 
    engineering team responds to any issues identified via the regular incident response and change management process\n\n
    '''

    heading = "3.5.6 Data Communications"

    response = {
        "heading" : heading,
        "paragraphs" : dc_3_main.split("\n\n"),
        "points" : [], 
        "table" : None
    }
    return response

def dc_3_6(system_name, provider):

    dc_3_main = f'''The boundaries of the {system_name} Platform are the specific aspects of the Company's infrastructure, 
    software, people, procedures, and data necessary to provide its services and that directly support the services provided to customers.
    Any infrastructure, software, people, procedures, and data that indirectly support the services provided to customers are not 
    included within the boundaries of the {system_name} Platform.\n\n
    This report does not include the Cloud Hosting Services provided by {provider} at multiple facilities.
    '''

    heading = "3.6 Boundaries of the System"

    response = {
        "heading" : heading,
        "paragraphs" : dc_3_main.split("\n\n"),
        "points" : [], 
        "table" : None
    }
    return response

def dc_4(incidents):

    dc_3_main = "No significant incidents have occurred to the services provided to user entities during the last 12 months."
    if incidents:
        dc_3_main = f'''Provide breach notifications for any identified system incidents that (a) were the result of controls that were 
        not suitably designed or operating effectively, or (b) otherwise resulted in a significant failure in the achievement of one or 
        more of those service commitments and system requirements in last 12 months, as of the date of the description (for a type 1 audit),
        or during the period of time covered by the description (for a type 2 audit), as applicable.
        '''
    

    heading = "DC 4: Disclosures about Identified Security Incidents"

    response = {
        "heading" : heading,
        "paragraphs" : dc_3_main.split("\n\n"),
        "points" : [], 
        "table" : None
    }
    return response

def dc_5():

    heading = "DC 5: The Applicable Trust Services Criteria and the Related Controls Designed to Provide Reasonable Assurance that the Service Organization's Service Commitments and System Requirements were Achieved"

    response = {
        "heading" : heading,
        "paragraphs" : [],
        "points" : [], 
        "table" : None
    }
    return response

def dc_5_1(company_name):

    dc_5_points = ["Formally, documented organizational policy statements and codes of conduct communicate entity values and behavioral standards to personnel.",
        "Policies and procedures require employees sign an acknowledgment form indicating they have been given access to the employee manual and understand their responsibility for adhering to the policies and procedures contained within the manual.",
        "A confidentiality statement agreeing not to disclose proprietary or confidential information, including client information, to unauthorized parties is a component of the employee handbook.",
        "Background checks are performed for employees as a component of the hiring process."]


    dc_3_main = f'''The effectiveness of controls cannot rise above the integrity and ethical values of the people who create, administer,
      and monitor them. Integrity and ethical values are essential elements of {company_name}'s control environment, affecting the design, 
      administration, and monitoring of other components. Integrity and ethical behavior are the product of {company_name}'s ethical and 
      behavioral standards, how they are communicated, and how they are reinforced in practices. They include management's actions to 
      remove or reduce incentives and temptations that might prompt personnel to engage in dishonest, illegal, or unethical acts. They 
      also include the communication of entity values and behavioral standards to personnel through policy statements and codes of 
      conduct, as well as by example.\n\n
      Specific control activities that the service organization has implemented in this area are described below:
        '''
    

    heading = "5.1 Integrity and Ethical Values"

    response = {
        "heading" : heading,
        "paragraphs" : dc_3_main.split("\n\n"),
        "points" : dc_5_points, 
        "table" : None
    }
    return response

def dc_5_2(company_name):

    dc_5_points = ["Management has considered the competence levels for particular jobs and translated required skills and knowledge levels into written position requirements.",
                    "Training is provided to maintain the skill level of personnel in certain positions."
                    ]


    dc_3_main = f'''{company_name}'s management defines competence as the knowledge and skills necessary to accomplish tasks that define 
    employees' roles and responsibilities. Management's commitment to competence includes management's consideration of the competence 
    levels for jobs and how those levels translate into the requisite skills and knowledge.\n\n
    Specific control activities that the service organization has implemented in this area are described below:

        '''
    

    heading = "5.2 Commitment to Competence"

    response = {
        "heading" : heading,
        "paragraphs" : dc_3_main.split("\n\n"),
        "points" : dc_5_points, 
        "table" : None
    }
    return response

def dc_5_3(company_name):

    dc_5_points = ["Management is periodically briefed on regulatory and industry changes affecting the services provided.",
            "Executive management meetings are held to discuss major initiatives and issues that affect the business."
            ]


    dc_3_main = f'''The {company_name} management team must balance two competing interests: continuing to grow and develop in a cutting edge,
      rapidly changing technology space while remaining excellent and conservative stewards of the highly-sensitive data and workflows
        our customers entrust to us.\n\n
        The management team meets frequently to be briefed on technology changes that impact the way {company_name} can help customers build data 
        workflows, as well as new security technologies that can help protect those workflows, and finally any regulatory changes that may
        require {company_name} to alter its software to maintain legal compliance. Major planned changes to the business are also reviewed by the 
        management team to ensure they can be conducted in a way that is compatible with our core product offerings and duties to new and 
        existing customers.\n\n
        Specific control activities that the service organization has implemented in this area are described below:
        '''
    

    heading = "5.3 Management's Philosophy and Operating Style"

    response = {
        "heading" : heading,
        "paragraphs" : dc_3_main.split("\n\n"),
        "points" : dc_5_points, 
        "table" : None
    }
    return response

def dc_5_4(company_name):

    dc_5_points = ["Organizational charts are in place to communicate key areas of authority and responsibility.",
            "Organizational charts are communicated to employees and updated as needed."
            ]


    dc_3_main = f'''{company_name}'s organizational structure provides the framework within which its activities for achieving entity-wide 
        objectives are planned, executed, controlled, and monitored. Management believes establishing a relevant organizational structure
        includes considering key areas of authority and responsibility. An organizational structure has been developed to suit its needs.
        This organizational structure is based, in part, on its size and the nature of its activities.\n\n
        {company_name}'s assignment of authority and responsibility activities include factors such as how authority and responsibility for operating 
        activities are assigned and how reporting relationships and authorization hierarchies are established. It also includes policies relating
        to appropriate business practices, knowledge, and experience of key personnel, and resources provided for carrying out duties. In 
        addition, it includes policies and communications directed at ensuring personnel understand the entity's objectives, know how their 
        individual actions interrelate and contribute to those objectives, and recognize how and for what they will be held accountable.\n\n
        Specific control activities that the service organization has implemented in this area are described below:

        '''
    

    heading = "5.4 Organizational Structure and Assignment of Authority and Responsibility"

    response = {
        "heading" : heading,
        "paragraphs" : dc_3_main.split("\n\n"),
        "points" : dc_5_points, 
        "table" : None
    }
    return response

async def dc_5_5(company_name):

    procedure_policy_text = parse_pdf_page(f"uploads/{company_name}_policy_packet.pdf", 1)

    try:
        response = await client.chat.completions.create(
            model="gpt-4o",
            temperature = 0.3,
            messages=[
            {"role": "system", "content": "You are an assistant that strictly provides answers based only on the provided content. Do not speculate, hallucinate, or provide information not directly found in the content."},
            {
                    "role": "user",
                    "content": (
                        f"Review the given content and check if the Table of contents has either 'code of conduct' or 'employee handbook' keeping the wording as it is, ignore the page number. Just return whichever one it is."
                        f"This is the table of contents: {procedure_policy_text}"
                    )
                }            
                ],
            
        )

        response_text = response.choices[0].message.content.strip()
        contents = response_text

    except Exception as e:
        contents = "(employee handbook/code of conduct)"

    dc_5_points = [f"New employees are required to sign acknowledgement forms for the {contents} and a confidentiality agreement following new hire orientation on their first day of employment.",
                "Evaluations for each employee are performed on an (annual/bi-annual/quaterly) basis.",
                "Personnel termination procedures are in place to guide the termination process and are documented in a termination checklist."
            ]


    dc_3_main = f'''{company_name}'s success is founded on sound business ethics, reinforced with a high level of efficiency, integrity, and
    ethical standards. The result of this success is evidenced by its proven track record for hiring and retaining top quality 
    personnel who ensures the service organization is operating at maximum efficiency. {company_name}'s human resources policies and practices 
    relate to employee hiring, orientation, training, evaluation, counseling, promotion, compensation, and disciplinary activities.\n\n
    Specific control activities that the service organization has implemented in this area are described below (Please Verify): 
    '''
    

    heading = "5.5 HR Policies and Practices"

    response = {
        "heading" : heading,
        "paragraphs" : dc_3_main.split("\n\n"),
        "points" : dc_5_points, 
        "table" : None
    }
    return response

def dc_5_6(company_name):

    dc_3_main = f'''{company_name}'s risk assessment process identifies and manages risks that could potentially affect {company_name}'s ability to 
    provide reliable and secure services to our customers. As part of this process, {company_name} maintains a risk register to track all systems 
    and procedures that could present risks to meeting the company's objectives. Risks are evaluated by likelihood and impact, and
      management creates tasks to address risks that score highly on both dimensions. The risk register is reevaluated annually, and 
      tasks are incorporated into the regular {company_name} product development process so they can be dealt with predictably and iteratively.'''
    

    heading = "5.6 Risk Assessment Process"

    response = {
        "heading" : heading,
        "paragraphs" : dc_3_main.split("\n\n"),
        "points" : [], 
        "table" : None
    }
    return response

def dc_5_7(company_name):

    dc_3_main = f'''The environment in which the system operates; the commitments, agreements, and responsibilities of {company_name}'s system; 
    as well as the nature of the components of the system result in risks that the criteria will not be met. {company_name} addresses these risks 
    through the implementation of suitably designed controls to provide reasonable assurance that the criteria are met. Because each 
    system and the environment in which it operates are unique, the combination of risks to meeting the criteria and the controls 
    necessary to address the risks will be unique. As part of the design and operation of the system, {company_name}'s management identifies the 
    specific risks that the criteria will not be met and the controls necessary to address those risks.
      '''
    

    heading = "5.7 Integration with Risk Assessment"

    response = {
        "heading" : heading,
        "paragraphs" : dc_3_main.split("\n\n"),
        "points" : [], 
        "table" : None
    }
    return response

def dc_5_8(company_name):

    dc_3_main = f'''Information and communication are an integral component of {company_name}'s internal control system. It is the process of 
    identifying, capturing, and exchanging information in the form and time frame necessary to conduct, manage, and control the entity's
    operations.\n\n
    {company_name} uses several information and communication channels internally to share information with management, employees, contractors, and 
    customers. {company_name} uses chat systems and email as the primary internal and external communications channels.\n\n
    Structured data is communicated internally via SaaS applications and project management tools. Finally, {company_name} uses in-person and video 
    “all hands” meetings to communicate company priorities and goals from management to all employees.

      '''
    

    heading = "5.8 Information and Communication Systems"

    response = {
        "heading" : heading,
        "paragraphs" : dc_3_main.split("\n\n"),
        "points" : [], 
        "table" : None
    }
    return response

def dc_5_9(company_name):

    dc_3_main = f'''Management monitors controls to ensure that they are operating as intended and that controls are modified as 
    conditions change. {company_name}'s management performs monitoring activities to continuously assess the quality of internal control over 
    time. Necessary corrective actions are taken as required to correct deviations from company policies and procedures. Employee activity 
    and adherence to company policies and procedures is also monitored. This process is accomplished through ongoing monitoring activities,
    separate evaluations, or a combination of the two.
      '''
    

    heading = "5.9 Monitoring Controls"

    response = {
        "heading" : heading,
        "paragraphs" : dc_3_main.split("\n\n"),
        "points" : [], 
        "table" : None
    }
    return response

def dc_5_9_1(company_name):

    dc_3_main = f'''{company_name}'s management conducts quality assurance monitoring on a regular basis and additional training is provided 
    based upon results of monitoring procedures. Monitoring activities are used to initiate corrective action through department meetings,
    internal conference calls, and informal notifications.\n\n
    Management's close involvement in {company_name}'s operations helps to identify significant variances from expectations regarding internal 
    controls. Upper management evaluates the facts and circumstances related to any suspected control breakdown. A decision for addressing 
    any control's weakness is made based on whether the incident was isolated or requires a change in the company's procedures or personnel. 
    The goal of this process is to ensure legal compliance and to maximize the performance of {company_name}'s personnel.

    '''
    

    heading = "5.9.1 On-going Monitoring"

    response = {
        "heading" : heading,
        "paragraphs" : dc_3_main.split("\n\n"),
        "points" : [], 
        "table" : None
    }
    return response

def dc_5_10():

    dc_3_main = f'''An internal risk management tracking tool is utilized to document and track the results of on-going monitoring
      procedures. Escalation procedures are maintained for responding and notifying management of any identified risks, and instructions 
      for escalation are supplied to employees in company policy documents. Risks receiving a high rating are responded to immediately. 
      Corrective actions, if necessary, are documented and tracked within the internal tracking tool. Annual risk meetings are held for 
      management to review reported deficiencies and corrective actions.

    '''
    

    heading = "5.10 Reporting Deficiencies"

    response = {
        "heading" : heading,
        "paragraphs" : dc_3_main.split("\n\n"),
        "points" : [], 
        "table" : None
    }
    return response

def dc_6(company_name, type):

    points_data = [
        f"User entities are responsible for understanding and complying with their contractual obligations to {company_name}.",
        f"User entities are responsible for notifying {company_name} of changes made to technical or administrative contact information.",
        f"User entities are responsible for maintaining their own system(s) of record.",
        f"User entities are responsible for ensuring the supervision, management, and control of the use of {company_name} services by their personnel.",
        f"User entities are responsible for developing their own disaster recovery and business continuity plans that address the inability to access or utilize {company_name} services.",
        f"User entities are responsible for providing {company_name} with a list of approvers for security and system configuration changes for data transmission.",
        f"User entities are responsible for immediately notifying {company_name} of any actual or suspected information security breaches, including compromised user accounts, including those used for integrations and secure file transfers."

    ]

    dc_2_main = f'''{company_name}'s services are designed with the assumption that certain controls will be implemented by user 
                    entities. Such controls are called complementary user entity controls. It is not feasible for all the Trust Services Criteria 
                    related to {company_name}'s services to be solely achieved by {company_name} control procedures. Accordingly, user entities, in conjunction with the
                    services, should establish their own internal controls or procedures to complement those of {company_name}'s.\n\n
                    The following complementary user entity controls should be implemented by user entities to provide additional assurance that the 
                    Trust Services Criteria described within this report are met. As these items represent only a part of the control considerations 
                    that might be pertinent at the user entities' locations, user entities' auditors should exercise judgment in selecting and reviewing
                    these complementary user entity controls.
                    '''

    heading = "DC 6: Complementary User Entity Controls"

    # table data will depend on type of report

    table_data_types =  {
        "SOC 2 Type I: Security" : {
            "Trust Services Criteria" : ["CC2.1", "CC6.2", "CC6.3", "CC6.6", "CC6.6"],
            "Complementary User Entity Controls" : [
                f"User entities are responsible for the security and integrity of data housed under user entity control, particularly the data utilized by {company_name} systems and services.",
                f"Determination of personnel who need specific functionality and the granting of such functionality is the responsibility of authorized personnel at the user entity. This includes allowing access to {company_name}'s application and API keys for access to the webservice API",
                "Authorized users and their associated access are reviewed periodically",
                f"User entities will ensure protective measures are in place for their data as it traverses from user entity to {company_name}.",
                f"User entities should establish adequate physical security and environmental controls of all devices and access points residing at their operational facilities, including remote employees or at-home agents for which the user entity allows connectivity in order to provide authorized information to {company_name}."
            ]
        }
    }

    response = {
        "heading" : heading,
        "paragraphs" : dc_2_main.split("\n\n"),
        "points" : points_data, 
        "table" : table_data_types[type]

    }
    return response

def dc_7(company_name,provider, type):

    dc_2_main = f'''Subservice Organizations\n\n
                    This report does not include the Cloud Hosting Services provided by {provider} at multiple facilities.\n\n
                    Subservice Description of Services\n\n
                    The Cloud Hosting Services provided by {provider} support the physical infrastructure of the entities services.\n\n
                    Complementary Subservice Organization Controls\n\n
                    {company_name}'s services are designed with the assumption that certain controls will be implemented by subservice organizations. Such controls are called complementary subservice organization controls. It is not feasible for all of the trust services criteria related to {company_name}'s services to be solely achieved by {company_name} control procedures.  Accordingly, subservice organizations, in conjunction with the services, should establish their own internal controls or procedures to complement those of {company_name}.\n\n
                    The following subservice organization controls have been implemented by {provider} and included in this report to provide additional assurance that the trust services criteria are met.\n\n
                    {provider}

                    '''

    heading = "DC 7: Complementary Subservice Organization Controls (CSOCs)"

    # table data will depend on type of report
    table_data_type = {
        "SOC 2 Type I: Security" : {
                "Category": [
                    "Security",
                    "Security",
                    "Security",
                    "Security",
                    "Security",
                    "Security",
                    "Security"
                ],
                "Criteria": [
                    "CC6.4",
                    "CC6.4",
                    "CC6.4",
                    "CC6.4",
                    "CC6.4",
                    "CC6.4",
                    "CC6.4"
                ],
                "Control": [
                    "Data center server floors, network rooms and security systems are physically isolated from public spaces and/or delivery areas.",
                    "Access to sensitive data center zones requires approval from authorized personnel and is controlled via badge access readers, biometric identification mechanism, and/or physical locks.",
                    "Data center perimeters are defined and secured via physical barriers.",
                    "Access lists to high security areas in data centers are reviewed on a defined basis and inappropriate access is removed in a timely manner.",
                    "Visitors to data center facilities must gain approval from authorized personnel, have their identity verified at the perimeter, and remain with an escort for the duration of the visit.",
                    "Security measures utilized in data centers are assessed annually and the results are reviewed by executive management.",
                    "Data centers are continuously staffed and monitored by security personnel using real time video surveillance and/or alerts generated by security systems."
                ]
            }

    }

    response = {
        "heading" : heading,
        "paragraphs" : dc_2_main.split("\n\n"),
        "points" : [], 
        "table" : table_data_type[type]

    }
    return response

def dc_7_ending(company_name):
    dc_3_main = f'''{company_name} management, along with the subservice provider, define the scope and responsibility of the controls necessary to meet all the 
                relevant trust services criteria through written contracts, such as service level agreements.  In addition, {company_name} performs monitoring of the subservice 
                organization controls, including the following procedures:
                '''

    heading = None

    points_data = [
                "Reviewing and reconciling output reports",
                "Holding periodic discussions with vendors and subservice organization(s)",
                "Making regular site visits to vendor and subservice organization(s') facilities",
                "Testing controls performed by vendors and subservice organization(s)",
                "Reviewing attestation reports over services provided by vendors and subservice organization(s)",
                "Monitoring external communications, such as customer complaints relevant to the services by the subservice organization"
    ]

    response = {
        "heading" : heading,
        "paragraphs" : dc_3_main.split("\n\n"),
        "points" : points_data, 
        "table" : None
    }
    return response

def dc_8(company_name, system):

    dc_3_main = f'''All Common Criteria/Security, Security criteria were applicable to the {company_name}'s {system} system.\n\n
    '''

    heading = "DC 8: Any Specific Criterion of the Applicable Trust Services Criteria that is Not Relevant to the System and the Reasons it is Not Relevant"

    response = {
        "heading" : heading,
        "paragraphs" : dc_3_main.split("\n\n"),
        "points" : [], 
        "table" : None
    }
    return response

def dc_9(changes):

    dc_3_main = f'''No significant changes have occurred to the services provided to user entities in the last 12 months preceding the end of the review date.
    '''
    points_data = []

    if changes:
        dc_3_main = f'''Examples of significant changes to a system include the following:\n\n
    ''' 
        points_data = ["Changes to the services provided",
    "Significant changes to IT and security personnel",
    "Significant changes to system processes, IT architecture and applications, and the processes and system used by subservice organizations",
    "Changes to legal and regulatory requirements that could affect system requirements",
    "Changes to organizational structure resulting in a change to internal control over the system (for example, a change to the legal entity)>"]


    heading = "DC 9: Disclosures of Significant Changes in Last 1 Year"

    response = {
        "heading" : heading,
        "paragraphs" : dc_3_main.split("\n\n"),
        "points" : points_data, 
        "table" : None
    }
    return response