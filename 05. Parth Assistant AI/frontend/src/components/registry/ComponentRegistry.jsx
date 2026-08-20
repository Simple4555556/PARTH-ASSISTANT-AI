import React from 'react';
import AttendanceCard from './AttendanceCard';
import RecentAttendance from './RecentAttendance';
import TimetableCard from './TimetableCard';
import StudentList from './StudentList';
import TeacherList from './TeacherList';
import AttendanceForm from './AttendanceForm';
import AttendanceAnalytics from './AttendanceAnalytics';
import DatabaseView from './DatabaseView';
import SupportRequest from './SupportRequest';
import NoticeList from './NoticeList';
import StudentDatabase from './StudentDatabase';
import ProfileCard from './ProfileCard';
import PolicyCard from './PolicyCard';


export const COMPONENT_MAP = {
  'attendance-card': AttendanceCard,
  'recent-attendance': RecentAttendance,
  'timetable-card': TimetableCard,
  'student-list': StudentList,
  'student-database': StudentDatabase,
  'teacher-list': TeacherList,
  'attendance-form': AttendanceForm,
  'mark-attendance': AttendanceForm,
  'attendance-analytics': AttendanceAnalytics,
  'database-view': DatabaseView,
  'support-request': SupportRequest,
  'notice-list': NoticeList,
  'profile-card': ProfileCard,
  'policy-card': PolicyCard
};


export function renderRegistryComponent(componentKey, props = {}) {
  if (!componentKey) return null;
  const Comp = COMPONENT_MAP[componentKey];
  if (!Comp) return null;
  return <Comp {...props} />;
}
