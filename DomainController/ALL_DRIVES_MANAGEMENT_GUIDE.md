# 🗂️ All Drives Management Guide
## Complete Drive Operations for A6_9V Domain Controller

---

## 📋 Available Drives

Your system has multiple drives that can be managed:

- **C:** - System Drive (Windows)
- **D:** - Data/Development Drive
- **E:** - Domain Controller Drive (M.2 1TB) - **PRIMARY**
- **F:** - Additional Storage Drive
- **H:** - Network/Cloud Drive (My Drive)

---

## 🚀 Quick Start - Run on All Drives

### Option 1: Sequential Drive Operations
Run Domain Controller operations on each drive one by one:

```batch
RUN_DRIVES_D_THEN_F.bat
```

This will:
1. Run on Drive D: first
2. Then switch to Drive F:
3. Show Domain Controller menu on each drive

---

### Option 2: Scan All Drives
Scan and analyze all drives:

```batch
ALL_DRIVES_SCAN.bat
```

---

### Option 3: Deploy to All Drives
Deploy Domain Controller to all drives:

```batch
DEPLOY_TO_ALL_DRIVES.bat
```

---

## 🔧 Drive-Specific Operations

### Drive E: (Primary - Domain Controller)
**Location:** `E:\DomainController`

**What's Here:**
- Main Domain Controller
- Secure Vault
- Trading Systems
- All core services

**Operations:**
```batch
cd E:\DomainController
START_HEAD_DOMAIN.bat
```

---

### Drive D: (Development/Data)
**Operations:**
- Run Domain Controller if installed
- Development projects
- Data storage

**Check for Domain Controller:**
```batch
cd D:\
if exist "DomainController" (
    cd DomainController
    START_HEAD_DOMAIN.bat
)
```

---

### Drive F: (Additional Storage)
**Operations:**
- Backup storage
- Additional projects
- Data archives

**Check for Domain Controller:**
```batch
cd F:\
if exist "DomainController" (
    cd DomainController
    START_HEAD_DOMAIN.bat
)
```

---

### Drive H: (Network/Cloud Drive)
**Location:** `H:\My Drive\`

**What's Here:**
- Cloud storage
- Trading systems
- Project files

**Operations:**
```batch
cd "H:\My Drive\storage-management"
python unified_trading_system.py
```

---

## 🎯 All Drives Management Scripts

### 1. Scan All Drives
Scans all drives for Domain Controller installations and reports status.

### 2. Deploy to All Drives
Deploys Domain Controller setup to all available drives.

### 3. Backup All Drives
Creates backups of important data from all drives.

### 4. Sync Across Drives
Synchronizes Domain Controller configuration across drives.

---

## 📊 Drive Status Check

Run this to check all drives:

```powershell
ALL_DRIVES_STATUS.ps1
```

This will show:
- Available drives
- Domain Controller installations
- Free space on each drive
- Drive health status

---

## 🔄 Drive Operations Workflow

### Daily Operations:
1. **Check All Drives:**
   ```batch
   ALL_DRIVES_STATUS.bat
   ```

2. **Run on Primary (E:):**
   ```batch
   cd E:\DomainController
   START_HEAD_DOMAIN.bat
   ```

3. **Backup Important Data:**
   ```batch
   BACKUP_ALL_DRIVES.bat
   ```

### Weekly Operations:
1. **Scan All Drives:**
   ```batch
   ALL_DRIVES_SCAN.bat
   ```

2. **Sync Configuration:**
   ```batch
   SYNC_DRIVES_CONFIG.bat
   ```

3. **Clean Up:**
   ```batch
   CLEANUP_ALL_DRIVES.bat
   ```

---

## 🛠️ Advanced Drive Management

### Multi-Drive Domain Controller
Run Domain Controller operations across multiple drives:

```batch
RUN_MULTI_DRIVE_CONTROLLER.bat
```

### Drive Health Monitoring
Monitor health of all drives:

```batch
MONITOR_ALL_DRIVES.bat
```

### Drive Optimization
Optimize all drives:

```batch
OPTIMIZE_ALL_DRIVES.bat
```

---

## 📝 Drive Configuration

### Primary Drive (E:)
- **Purpose:** Main Domain Controller
- **Status:** Active
- **Services:** All core services

### Secondary Drives (D:, F:)
- **Purpose:** Backup, Development, Storage
- **Status:** Available
- **Services:** Optional Domain Controller instances

### Network Drive (H:)
- **Purpose:** Cloud storage, Trading systems
- **Status:** Network connected
- **Services:** Trading system files

---

## 🚨 Drive Troubleshooting

### If Drive Not Detected:
1. Check if drive is connected
2. Verify drive letter assignment
3. Check disk management

### If Domain Controller Not Found on Drive:
1. Check if DomainController folder exists
2. Verify installation
3. Deploy if needed

### If Drive Full:
1. Run cleanup script
2. Move data to other drives
3. Delete unnecessary files

---

## 🎯 Recommended Next Steps for All Drives

1. **Scan All Drives:**
   - Identify all available drives
   - Check for Domain Controller installations
   - Report drive status

2. **Deploy to Secondary Drives:**
   - Install Domain Controller on D: and F:
   - Sync configuration
   - Set up backups

3. **Set Up Drive Monitoring:**
   - Enable health monitoring
   - Set up alerts
   - Schedule regular scans

4. **Configure Backup Strategy:**
   - Set up automated backups
   - Configure backup locations
   - Test restore procedures

---

*Last Updated: November 14, 2025*
*Team A6_9V - All Drives Management*
