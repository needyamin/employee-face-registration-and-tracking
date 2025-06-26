# Employee Face Recognition System

A modern, user-friendly employee face recognition and tracking system built with Python, Tkinter, and OpenCV. This application allows companies to register employees with facial recognition, manage employee databases, and perform real-time face tracking.

## 🚀 Features

### Core Functionality
- **Face Registration**: Upload employee photos and register them with facial recognition
- **Employee Management**: Add, delete, and search employees with a modern UI
- **Real-time Tracking**: Live camera face detection and recognition
- **Database Storage**: Persistent SQLite database for employee data
- **Movement Logging**: Automatic logging of employee movements

### User Interface
- **Modern Design**: Clean, professional interface with ttk themed widgets
- **Tabbed Interface**: Organized tabs for Registration, Employee List, and Tracking
- **Search Functionality**: Real-time search through employee database
- **Employee Details**: Double-click to view employee information
- **Progress Indicators**: Visual feedback during face registration
- **Status Bar**: Real-time status updates and tooltips
- **Responsive Layout**: Grid-based layout with proper spacing

### Technical Features
- **Multi-threading**: Non-blocking UI during face processing
- **Error Handling**: Comprehensive error handling and user feedback
- **Data Persistence**: SQLite database with image and encoding storage
- **Face Detection**: RetinaFace for accurate face detection and alignment
- **Image Processing**: PIL for image manipulation and display

## 📋 Requirements

### System Requirements
- Python 3.7 or higher
- Webcam (for face tracking)
- Windows/Linux/macOS

### Python Dependencies
```
retina-face
opencv-python
Pillow
numpy
tf-keras
```

## 🛠️ Installation

### Step 1: Clone or Download
```bash
git clone https://github.com/needyamin/employee-face-registration-and-tracking
cd face-detection
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Run the Application
```bash
python face_detection.py
```

## 📖 Usage Guide

### 1. Employee Registration
1. **Navigate to Register Tab**: Click on the "Register Face" tab
2. **Enter Employee Name**: Type the employee's full name
3. **Upload Image**: Click "Upload Image" and select a clear photo of the employee
4. **Register Face**: Click "Register Face" to process and save the employee data
5. **Confirmation**: Wait for the success message

### 2. Employee Management
1. **View Employees**: Go to the "Employee List" tab to see all registered employees
2. **Search Employees**: Use the search bar to find specific employees
3. **View Details**: Double-click on an employee to see their details
4. **Delete Employee**: Select an employee and click "Delete Employee"
5. **Refresh List**: Click "Refresh List" to update the display

### 3. Face Tracking
1. **Start Tracking**: Go to the "Tracking" tab and click "Start Tracking"
2. **Camera Access**: Allow camera access when prompted
3. **Real-time Detection**: The system will detect and identify registered employees
4. **Stop Tracking**: Press ESC in the camera window to stop tracking

## 📁 Project Structure

```
face-detection/
├── face_detection.py      # Main application file
├── data.py               # Database management module
├── requirements.txt      # Python dependencies
├── README.md            # This file
├── faces.db             # SQLite database (created automatically)
└── movement_log.txt     # Employee movement logs (created automatically)
```

### File Descriptions

#### `face_detection.py`
- Main GUI application
- Face registration and tracking logic
- User interface components
- Multi-threading implementation

#### `data.py`
- SQLite database operations
- User data management
- Image and encoding storage
- Database initialization

#### `requirements.txt`
- List of required Python packages
- Version specifications for compatibility

## 🔧 Configuration

### Company Name
To change the company name displayed in the application:
```python
# In face_detection.py, line ~330
company_name = "YOUR COMPANY NAME"
```

### Database Location
The SQLite database is stored in the same directory as the application:
```python
# In data.py
DB_PATH = 'faces.db'
```

### Face Detection Threshold
Adjust the face recognition sensitivity:
```python
# In face_detection.py, tracking function
if distance < 30:  # Lower value = more strict matching
```

## 🐛 Troubleshooting

### Common Issues

#### 1. Camera Not Accessible
- **Error**: "Unable to access the camera"
- **Solution**: Check camera permissions and ensure no other application is using the camera

#### 2. Face Not Detected
- **Error**: "No face detected"
- **Solution**: 
  - Use a clear, well-lit photo
  - Ensure the face is clearly visible
  - Try different angles or lighting

#### 3. Employee List Not Showing
- **Issue**: Empty employee list
- **Solutions**:
  - Register at least one employee first
  - Check if the database file exists
  - Verify registration was successful

#### 4. Import Errors
- **Error**: Missing module errors
- **Solution**: Install all dependencies with `pip install -r requirements.txt`

#### 5. Database Errors
- **Error**: SQLite database issues
- **Solution**: Delete `faces.db` file and restart the application

### Performance Tips

1. **Image Quality**: Use high-quality, well-lit photos for better recognition
2. **Database Size**: Regularly clean up unused employee records
3. **System Resources**: Close other applications when using face tracking
4. **Lighting**: Ensure good lighting for real-time face detection

## 🔒 Security Considerations

- **Local Storage**: All data is stored locally on your machine
- **No Network**: The application doesn't require internet connection
- **Privacy**: Employee photos and data remain on your system
- **Access Control**: Implement additional security measures for production use

## 🚀 Future Enhancements

### Planned Features
- [ ] Employee ID and department fields
- [ ] Export/import employee data
- [ ] Attendance tracking
- [ ] Multiple camera support
- [ ] Advanced face recognition algorithms
- [ ] User authentication system
- [ ] Backup and restore functionality
- [ ] Dark mode theme
- [ ] Mobile app integration

### Contributing
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👥 Support

For support and questions:
- Create an issue in the repository
- Check the troubleshooting section
- Review the code comments for implementation details

## 🎯 Use Cases

### Business Applications
- **Office Security**: Track employee access to secure areas
- **Attendance System**: Monitor employee presence
- **Visitor Management**: Identify authorized personnel
- **Time Tracking**: Log employee entry and exit times

### Educational Institutions
- **Student Attendance**: Track student presence in classes
- **Campus Security**: Monitor access to restricted areas
- **Library Management**: Control access to resources

### Healthcare
- **Patient Identification**: Verify patient identity
- **Staff Access**: Control access to medical areas
- **Visitor Tracking**: Monitor hospital visitors

---

**Version**: 1.0.0  
**Last Updated**: 27 June 2025
**Author**: ANSNEW TECH. 
