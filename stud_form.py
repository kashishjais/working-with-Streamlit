#streamlit run stud_form.py  OR
# py -m streamlit run stud_form.py

import streamlit as st
from data import open_db
from data import Student,Grade

def show_student_form():
    with st.form('f1'):
        name=st.text_input("enter student name")
        c1,c2=st.columns(2)
        klass=c1.text_input("enter student class")
        section=c2.text_input("enter student section")
        is_online=st.checkbox("is student attending online?")
        btn=st.form_submit_button("add student")

    if btn and name and klass and section:
        db=open_db()
        db.add(Student(name=name,section=section,klass=klass,is_online=is_online)) 
        db.commit()
        db.close()
        st.success("saved student details")   
def show_grading_form():
    with st.form('f2'):
        id=st.text_input("enter student id/rollno")
        student=st.text_input("enter student name")
        c1,c2,c3=st.columns(3)
        hindi=c1.text_input("enter hindi marks")
        english=c2.text_input("enter english marks")
        maths=c3.text_input("enter maths marks")
        total=st.text_input("enter total marks")
        btn=st.form_submit_button("add grade")
    if btn and id  and student and hindi and english and maths and total:
        db=open_db()
        db.add(Grade(id=id,student=student,hindi=hindi,english=english,maths=maths,total=total)) 
        db.commit()
        db.close()
        st.success("saved student grades")       

def show_students_data():
    db=open_db()
    student_list=db.query(Student).all()
    db.close()
    for student in student_list:
        with st.expander(f"student detail {student.name}",True):
            st.subheader(student.name)
            st.markdown(f'''
            - class : {student.klass}
            - section : {student.section}
            - online : {'✅' if student.is_online else '🚫'}
            - admit date : {student.admit_date}''')
            btn=st.button(f"delete{student.name}")
            if btn:
                db=open_db()
                std=db.query(Student).get(student.id)
                db.delete(std)
                db.commit()
                db.close()
                st.success("deletion completed,press R to refresh list")

def find_student():
    with st.form("search form"):
        params=['id','name','section','class']
        c1,c2=st.columns(2)
        by=c1.selectbox('Search Student by ',options=params)
        query=c2.text_input("type keyword here ")
        btn=st.form_submit_button("search")
    
    result=None
    db=open_db()
    if btn and query:
        if by==params[0]:
             result=db.query(Student).filter(Student.id==query)
        if by==params[1]:
             result=db.query(Student).filter(Student.name==query)     
        if by==params[2]:
             result=db.query(Student).filter(Student.section==query)
        if by==params[3]:
             result=db.query(Student).filter(Student.klass==query)     
    if result:
        count=result.count()
        if count==1:
            student=result.all()[0]
            st.info("student details found")
            st.markdown(f'''
            ### {student.name}
            - class : {student.klass}
            - section : {student.section}
            - online : {'✅' if student.is_online else '🚫'}
            - admit date : {student.admit_date}''')
        elif count>1:
            for student in result.all():
                st.markdown(f'''
                ### {student.name}
                - class : {student.klass}
                - section : {student.section}
                - online : {'✅' if student.is_online else '🚫'}
                - admit date : {student.admit_date}
                ----
                ''')    
    db.close()
        

st.title("Database Example for Newbies😎😎")

options=["View students","find student","add students","add grades"]
choice=st.sidebar.radio("select any option",options)

if choice==options[0]:
    show_students_data()
elif choice==options[1]:
    find_student()
elif choice==options[2]:
    show_student_form()
elif choice==options[3]:
    show_grading_form()
