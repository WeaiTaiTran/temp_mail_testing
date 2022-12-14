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
    response = requests.post(url=API_ORG_LIBRARY, headers=headers.headers, json={"query": query, "variables": variables})
    print(response.json())
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
                "name": "???ng d???ng ?????o h??m ????? kh???o s??t v?? v??? ????? th??? h??m s???",
                "children": [
                    {
                    "name": "T??nh ????n ??i???u c???a h??m s???",
                    "children": []
                    },
                    {
                    "name": "C???c tr??? c???a h??m s???",
                    "children": []
                    },
                    {
                    "name": "Gi?? tr??? l???n nh???t - Gi?? tr??? nh??? nh???t c???a h??m s???",
                    "children": []
                    },
                    {
                    "name": "???????ng ti???m c???n",
                    "children": []
                    },
                    {
                    "name": "S??? bi???n thi??n v?? ????? th??? h??m s???",
                    "children": []
                    },
                    {
                    "name": "T????ng giao ????? th???",
                    "children": []
                    },
                    {
                    "name": "Ti???p tuy???n c???a ????? th??? h??m s???",
                    "children": []
                    }
                ]
                },
                {
                "name": "H??m s??? l??y th???a - H??m s??? m?? - H??m s??? l??garit",
                "children": [
                    {
                    "name": "L??y th???a",
                    "children": []
                    },
                    {
                    "name": "L??garit",
                    "children": []
                    },
                    {
                    "name": "H??m s??? l??y th???a - H??m s??? m?? - H??m s??? l??garit",
                    "children": []
                    },
                    {
                    "name": "Ph????ng tr??nh m??",
                    "children": []
                    },
                    {
                    "name": "Ph????ng tr??nh l??garit",
                    "children": []
                    },
                    {
                    "name": "B???t ph????ng tr??nh m??",
                    "children": []
                    },
                    {
                    "name": "B???t ph????ng tr??nh l??garit",
                    "children": []
                    }
                ]
                },
                {
                "name": "Nguy??n h??m - T??ch ph??n v?? ???ng d???ng",
                "children": [
                    {
                    "name": "Nguy??n h??m",
                    "children": []
                    },
                    {
                    "name": "T??ch ph??n",
                    "children": []
                    },
                    {
                    "name": "Di???n t??ch h??nh ph???ng",
                    "children": []
                    },
                    {
                    "name": "Th??? t??ch v???t th???",
                    "children": []
                    }
                ]
                },
                {
                "name": "S??? ph???c",
                "children": [
                    {
                    "name": "C??c y???u t??? c???a s??? ph???c",
                    "children": []
                    },
                    {
                    "name": "C??c ph??p to??n tr??n t???p s??? ph???c",
                    "children": []
                    },
                    {
                    "name": "Ph????ng tr??nh - H??? ph????ng tr??nh",
                    "children": []
                    },
                    {
                    "name": "T???p h???p ??i???m bi???u di???n s??? ph???c",
                    "children": []
                    },
                    {
                    "name": "C???c tr??? s??? ph???c",
                    "children": []
                    }
                ]
                },
                {
                "name": "Kh???i ??a di???n - Th??? t??ch kh???i ??a di???n",
                "children": [
                    {
                    "name": "Kh??i ni???m v??? kh???i ??a di???n",
                    "children": []
                    },
                    {
                    "name": "Th??? t??ch kh???i ch??p",
                    "children": []
                    },
                    {
                    "name": "Th??? t??ch kh???i l??ng tr???",
                    "children": []
                    },
                    {
                    "name": "T??? s??? th??? t??ch",
                    "children": []
                    }
                ]
                },
                {
                "name": "M???t n??n - M???t tr??? - M???t c???u",
                "children": [
                    {
                    "name": "M???t n??n",
                    "children": []
                    },
                    {
                    "name": "M???t tr???",
                    "children": []
                    },
                    {
                    "name": "M???t c???u",
                    "children": []
                    }
                ]
                },
                {
                "name": "Ph????ng ph??p t???a ????? trong kh??ng gian",
                "children": [
                    {
                    "name": "H??? tr???c t???a ????? trong kh??ng gian",
                    "children": []
                    },
                    {
                    "name": "Ph????ng tr??nh m???t ph???ng",
                    "children": []
                    },
                    {
                    "name": "Ph????ng tr??nh ???????ng th???ng",
                    "children": []
                    },
                    {
                    "name": "V??? tr?? t????ng ?????i",
                    "children": []
                    },
                    {
                    "name": "G??c",
                    "children": []
                    },
                    {
                    "name": "Kho???ng c??ch",
                    "children": []
                    },
                    {
                    "name": "Ph????ng tr??nh m???t c???u",
                    "children": []
                    },
                    {
                    "name": "C???c tr??? h??nh h???c",
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
                "Si??u d???",
                "B??nh th?????ng",
                "Kh??"
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