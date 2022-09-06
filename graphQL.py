import requests

API_CLASSROOM = "https://api.data-advising.net/classroom/v1/graphql"
API_STUDENT = "https://api.data-advising.net/student/v1/graphql"
API_ORG_STUDENT = "https://api.data-advising.net/weai/student/v1/graphql"
API_ORG_LIBRARY = "https://api.data-advising.net/weai/library/v1/graphql"
API_ORG_CLASSROOM = "https://api.data-advising.net/weai/classroom/v1/graphql"

class Headers :
    TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOiJodHRwczovL2FwaS5kYXRhLWFkdmlzaW5nLm5ldC91c2VyL3YxIiwiaWF0IjoxNjYyNDQ4NjM0MjIwLCJleHAiOjE2NjI1MzUwMzQyMjAsInN1YiI6InRhaXRyYW4yNzEyMDFAZ21haWwuY29tIiwidXNlcl9pZCI6NTMyMSwidXNlcl9uYW1lIjoidGFpdHJhbjI3MTIwMSIsInNpZ25faW5fdHlwZSI6IkdPT0dMRSIsInRva2VuX3R5cGUiOiJCZWFyZXIifQ.lKbq-sfZ3WESELUxZcNXPoECwk1Tnj0g1TwuMm-iSUI"
    bearerToken = f"bearer {TOKEN}"
    headers = {'Authorization': bearerToken}

    def __init__(self):
        self.checkAccessToken()  

    def checkAccessToken(self):
        if not self.TOKEN :
            print("Token Not Valid")
            self.updateToken()
        else:
            res = self.getProfile()
            # print(res)
            if res['data']['getProfile']['errors'] is None:
                print(f"Token valid: {self.TOKEN}")
            else:
                self.updateToken()
                self.checkAccessToken()
    
    def updateToken(self):
        self.TOKEN = getAccessToken()['data']['signIn']['auth_token']['id_token']['token']
        self.bearerToken = f"bearer {self.TOKEN}"
        self.headers = {'Authorization': self.bearerToken}
        
    def getProfile(self):
        query = '''{
            getProfile {
                status
                message
                errors {
                message
                error_code
                __typename
                }
                student {
                user_id
                user_name
                url_avatar
                last_name
                first_name
                email
                birth_date
                phone_number {
                    area_code
                    phone
                    __typename
                }
                gender
                address {
                    country
                    city
                    detail
                    __typename
                }
                personal_quote
                social_links {
                    link
                    name
                    __typename
                }
                school
                teacher
                organizations {
                    code
                    name
                    short_name
                    logo
                    banner
                    short_description
                    is_owner
                    __typename
                }
                __typename
                }
                __typename
            }
        }
        '''
        response = requests.post(url=API_STUDENT, headers=self.headers, json={"query": query})
        return response.json()

def getAccessToken():
    query = '''# Write your query or mutation here
    mutation (
    $email: String
    $password: String
    $remember_me: Boolean
    $code: String
    $state: String
    $sign_in_type: SignInType!
    ) {
    signIn(
        input: {
        email: $email
        password: $password
        remember_me: $remember_me
        state: $state
        code: $code
        sign_in_type: $sign_in_type
        }
    ) {
        status
        message
        errors {
        error_code
        message
        error_fields
        }
        auth_token {
        id_token {
            token
            expired_time
        }
        refresh_token {
            token
            expired_time
        }
        }
        __typename
    }
    }'''

    variables = {
        "sign_in_type": "EMAIL",
        "email": "taitran271201@gmail.com",
        "password": "weai123@",
        "remember_me": False
    }

    response = requests.post(url=API_STUDENT, json={"query": query, "variables": variables})
    return response.json()

headers = Headers()

def createClassroom(className):
    query = '''mutation createClassroom($inputs: ClassroomInput!) {
    createClassroom(inputs: $inputs) {
            status
            message
            data {
            code
            id
            __typename
            }
            errors {
            message
            error_code
            __typename
            }
            __typename
        }
    }'''
    variables =     {
        "inputs": {
            "name": className,
            "registration": [
            "first_name",
            "last_name",
            "phone__area_code",
            "phone__phone",
            "address__city",
            "address__detail",
            "address__country",
            "school_name",
            "student_code"
            ]
        }
    }
    response = requests.post(url=API_ORG_CLASSROOM, headers=headers.headers, json={"query": query, "variables": variables})
    return response.json()

def SendMail(classID, listMail):
    query = '''mutation SendMail($inputs: sendMailInput!) {
        sendMail(inputs: $inputs) {
            status
            message
            errors {
            message
            error_code
            __typename
            }
            __typename
        }
    }
    '''
    variables = {
        "inputs": {
            "emails": listMail,
            "classroom_id": classID
        }
    }
    response = requests.post(url=API_CLASSROOM, headers=headers.headers, json={"query": query, "variables": variables})
    print(response.json())
    return response.json()

def SendMailOrg(classID, role, listMail):
    query = '''mutation SendMail($inputs: sendMailInput!) {
        sendMail(inputs: $inputs) {
            status
            message
            errors {
            message
            error_fields
            error_code
            __typename
            }
            __typename
        }
    }
    '''
    variables = {
        "emails": listMail,
        "classroom_id": classID,
        "role": role
    }
    response = requests.post(url=API_CLASSROOM, headers=headers.headers, json={"query": query, "variables": variables})
    return response.json()

def addOrganizationUsers(listMail):
    query = '''mutation addOrganizationUsers($emails: [String]!) {
        addOrganizationUsers(emails: $emails) {
            status
            message
            errors {
            message
            error_code
            error_fields
            __typename
            }
            __typename
        }
    }
    '''
    variables = {
        "emails": listMail
    }
    response = requests.post(url=API_ORG_STUDENT, headers=headers.headers, json={"query": query, "variables": variables})
    return response.json()

def addSubjectPermissions(listMail, subjectID):
    query = '''mutation addSubjectPermissions($emails: [String!], $subject_id: Int!) {
        addSubjectPermissions(emails: $emails, subject_id: $subject_id) {
            status
            message
            errors {
            message
            error_code
            error_fields
            __typename
            }
            __typename
        }
    }
    '''
    variables = {
        "emails": listMail,
        "subject_id": subjectID
    }
    response = requests.post(url=API_ORG_STUDENT, headers=headers.headers, json={"query": query, "variables": variables})
    return response.json()

def createSubject(subjectName):
    query = '''mutation createSubject($subject: SubjectInput) {
        createSubject(subject: $subject) {
            status
            message
            errors {
            message
            error_code
            error_fields
            __typename
            }
            data {
            ... on Subject {
                id
                __typename
            }
            __typename
            }
            __typename
        }
    }
    '''
    variables = {
        "subject": {
            "name": subjectName,
            "categories": {
            "name": subjectName,
            "children": [
                {
                "name": "Ứng dụng đạo hàm để khảo sát và vẽ đồ thị hàm số",
                "children": [
                    {
                    "name": "Tính đơn điệu của hàm số",
                    "children": []
                    },
                    {
                    "name": "Cực trị của hàm số",
                    "children": []
                    },
                    {
                    "name": "Giá trị lớn nhất - Giá trị nhỏ nhất của hàm số",
                    "children": []
                    },
                    {
                    "name": "Đường tiệm cận",
                    "children": []
                    },
                    {
                    "name": "Sự biến thiên và đồ thị hàm số",
                    "children": []
                    },
                    {
                    "name": "Tương giao đồ thị",
                    "children": []
                    },
                    {
                    "name": "Tiếp tuyến của đồ thị hàm số",
                    "children": []
                    }
                ]
                },
                {
                "name": "Hàm số lũy thừa - Hàm số mũ - Hàm số lôgarit",
                "children": [
                    {
                    "name": "Lũy thừa",
                    "children": []
                    },
                    {
                    "name": "Lôgarit",
                    "children": []
                    },
                    {
                    "name": "Hàm số lũy thừa - Hàm số mũ - Hàm số lôgarit",
                    "children": []
                    },
                    {
                    "name": "Phương trình mũ",
                    "children": []
                    },
                    {
                    "name": "Phương trình lôgarit",
                    "children": []
                    },
                    {
                    "name": "Bất phương trình mũ",
                    "children": []
                    },
                    {
                    "name": "Bất phương trình lôgarit",
                    "children": []
                    }
                ]
                },
                {
                "name": "Nguyên hàm - Tích phân và ứng dụng",
                "children": [
                    {
                    "name": "Nguyên hàm",
                    "children": []
                    },
                    {
                    "name": "Tích phân",
                    "children": []
                    },
                    {
                    "name": "Diện tích hình phẳng",
                    "children": []
                    },
                    {
                    "name": "Thể tích vật thể",
                    "children": []
                    }
                ]
                },
                {
                "name": "Số phức",
                "children": [
                    {
                    "name": "Các yếu tố của số phức",
                    "children": []
                    },
                    {
                    "name": "Các phép toán trên tập số phức",
                    "children": []
                    },
                    {
                    "name": "Phương trình - Hệ phương trình",
                    "children": []
                    },
                    {
                    "name": "Tập hợp điểm biểu diễn số phức",
                    "children": []
                    },
                    {
                    "name": "Cực trị số phức",
                    "children": []
                    }
                ]
                },
                {
                "name": "Khối đa diện - Thể tích khối đa diện",
                "children": [
                    {
                    "name": "Khái niệm về khối đa diện",
                    "children": []
                    },
                    {
                    "name": "Thể tích khối chóp",
                    "children": []
                    },
                    {
                    "name": "Thể tích khối lăng trụ",
                    "children": []
                    },
                    {
                    "name": "Tỉ số thể tích",
                    "children": []
                    }
                ]
                },
                {
                "name": "Mặt nón - Mặt trụ - Mặt cầu",
                "children": [
                    {
                    "name": "Mặt nón",
                    "children": []
                    },
                    {
                    "name": "Mặt trụ",
                    "children": []
                    },
                    {
                    "name": "Mặt cầu",
                    "children": []
                    }
                ]
                },
                {
                "name": "Phương pháp tọa độ trong không gian",
                "children": [
                    {
                    "name": "Hệ trục tọa độ trong không gian",
                    "children": []
                    },
                    {
                    "name": "Phương trình mặt phẳng",
                    "children": []
                    },
                    {
                    "name": "Phương trình đường thẳng",
                    "children": []
                    },
                    {
                    "name": "Vị trí tương đối",
                    "children": []
                    },
                    {
                    "name": "Góc",
                    "children": []
                    },
                    {
                    "name": "Khoảng cách",
                    "children": []
                    },
                    {
                    "name": "Phương trình mặt cầu",
                    "children": []
                    },
                    {
                    "name": "Cực trị hình học",
                    "children": []
                    }
                ]
                }
            ]
            },
            "configs": {
            "question": {
                "levels": [
                1,
                2,
                3,
                4
                ],
                "addition_configs": []
            },
            "exam": {
                "times": [
                15,
                45,
                60,
                90
                ],
                "ranks": [
                "Siêu dễ",
                "Bình thường",
                "Khó"
                ],
                "addition_configs": []
            },
            "lecture": {
                "addition_configs": []
            }
            },
            "hashtags": [],
            "status": "ACTIVE"
        }
    }

    response = requests.post(url=API_ORG_STUDENT, headers=headers.headers, json={"query": query, "variables": variables})
    return response.json()