# XDCAM-Repair-Tool

# MTS
![Screenshot from 2024-06-01 10-51-53](https://github.com/DRCRecoveryData/XDCAM-Repair-Tool/assets/85211068/efc0170f-604c-4b65-bd49-f39d1a3387ca)


# MXF
![Screenshot from 2024-06-01 10-50-42](https://github.com/DRCRecoveryData/XDCAM-Repair-Tool/assets/85211068/8c64c316-11cb-4621-92e8-4a6d312f57c6)


This is a PyQt6-based desktop application for repairing corrupted video files. The tool supports repairing two types of video files: MTS and MXF. It can automatically detect the file extension of the reference file to determine the type of files to repair.

## Features:
- Repair corrupted MTS files.
- Repair corrupted MXF files.
- Automatic detection of file extension for reference file.
- Option to convert repaired files to another format.
- Progress bar to track repair process.
- Log box to display repair progress and messages.
- Cross-platform compatibility (Windows, macOS, Linux).

## How to Use:
1. Select the reference file (MTS or MXF) used for repair.
2. Choose the folder containing the corrupted video files.
3. Optionally, select the option to convert repaired files to another format.
4. Click the "Repair" button to start the repair process.
5. Monitor the repair progress in the progress bar and log box.
6. Once the repair is complete, repaired files will be saved in the "Repaired" folder, and if conversion was selected, converted files will be saved in the "Converted" folder.

## Technologies Used:
- Python 3
- PyQt6

```pip install pyqt6```

## Contributions:
Contributions are welcome! If you encounter any issues or have suggestions for improvements, feel free to open an issue or submit a pull request.

GitHub Repository: [https://github.com/DRCRecoveryData/XDCAM-Repair-Tool](https://github.com/DRCRecoveryData/XDCAM-Repair-Tool)
