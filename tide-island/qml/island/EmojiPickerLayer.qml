import QtQuick
import QtQuick.Controls.Basic
import Quickshell
import "EmojiData.js" as EmojiData

FocusScope {
    id: root
    focus: true

    property string iconFontFamily: ""
    property string textFontFamily: ""
    property string heroFontFamily: ""
    property bool showCondition: false

    signal closeRequested()

    anchors.fill: parent
    visible: opacity > 0
    opacity: showCondition ? 1 : 0

    Behavior on opacity {
        NumberAnimation {
            duration: 180
            easing.type: Easing.InOutQuad
        }
    }

    // Properties for emoji picker
    property int selectedCategoryIndex: 0
    property string selectedCategory: EmojiData.CATEGORIES[selectedCategoryIndex].id
    property int selectedIndex: 0
    property string searchText: ""

    // Columns configuration
    readonly property int columns: 12
    readonly property int itemWidth: (width - 32 - (columns - 1) * 10) / columns
    readonly property int itemHeight: 44

    readonly property var filteredEmojis: {
        if (searchText.trim() === "") {
            const cat = EmojiData.CATEGORIES[selectedCategoryIndex].id;
            return EmojiData.EMOJIS.filter(function(e) {
                return e.category === cat;
            });
        }
        const query = searchText.toLowerCase().trim();
        return EmojiData.EMOJIS.filter(function(e) {
            return e.name.indexOf(query) !== -1 || e.keywords.indexOf(query) !== -1;
        });
    }

    // Defer active focus to text field to prevent Wayland focus racing
    Timer {
        id: focusTimer
        interval: 10
        repeat: false
        onTriggered: searchInput.forceActiveFocus()
    }

    onShowConditionChanged: {
        if (showCondition) {
            searchText = "";
            selectedIndex = 0;
            selectedCategoryIndex = 0;
            focusTimer.restart();
        }
    }

    onSearchTextChanged: {
        selectedIndex = 0;
    }

    onSelectedCategoryIndexChanged: {
        selectedIndex = 0;
    }

    onSelectedIndexChanged: {
        if (filteredEmojis.length === 0) return;
        const row = Math.floor(selectedIndex / columns);
        const yPos = row * (itemHeight + 10);
        
        if (yPos < flickable.contentY) {
            flickable.contentY = yPos;
        } else if (yPos + itemHeight > flickable.contentY + flickable.height) {
            flickable.contentY = yPos + itemHeight - flickable.height;
        }
    }

    function copyEmoji(emojiStr) {
        if (!emojiStr) return;
        Quickshell.execDetached(["sh", "-c", "echo -n " + JSON.stringify(emojiStr) + " | wl-copy"]);
        root.closeRequested();
    }

    // Main Layout wrapper
    Column {
        anchors.fill: parent
        anchors.margins: 18
        spacing: 12

        // Search Bar Input Container (Ultra-Premium Dynamic Island Style, NO BORDER)
        Rectangle {
            id: searchBarContainer
            width: parent.width
            height: 44
            radius: 14
            color: Qt.rgba(1, 1, 1, 0.05)
            border.width: 0

            Row {
                anchors.fill: parent
                anchors.leftMargin: 16
                anchors.rightMargin: 16
                spacing: 12

                Text {
                    id: searchIcon
                    text: ""
                    font.family: root.iconFontFamily
                    font.pixelSize: 14
                    color: searchInput.activeFocus ? "#ffffff" : Qt.rgba(1, 1, 1, 0.35)
                    anchors.verticalCenter: parent.verticalCenter
                }

                TextField {
                    id: searchInput
                    focus: true
                    width: parent.width - searchIcon.width - (clearButton.visible ? clearButton.width : 0) - 40
                    height: parent.height
                    anchors.verticalCenter: parent.verticalCenter
                    
                    placeholderText: qsTr("Search emojis...")
                    placeholderTextColor: Qt.rgba(1, 1, 1, 0.3)
                    color: "#ffffff"
                    
                    font.family: root.textFontFamily
                    font.pixelSize: 14
                    
                    background: null
                    leftPadding: 0
                    rightPadding: 0
                    topPadding: 0
                    bottomPadding: 0
                    verticalAlignment: TextInput.AlignVCenter
                    
                    text: root.searchText
                    onTextChanged: root.searchText = text

                    Keys.onPressed: (event) => {
                        const cols = root.columns;
                        if (event.key === Qt.Key_Tab) {
                            if (root.searchText === "") {
                                let nextIdx = (root.selectedCategoryIndex + (event.modifiers & Qt.ShiftModifier ? -1 : 1) + EmojiData.CATEGORIES.length) % EmojiData.CATEGORIES.length;
                                root.selectedCategoryIndex = nextIdx;
                                event.accepted = true;
                            }
                        } else if (event.key === Qt.Key_Down) {
                            if (root.filteredEmojis.length > 0) {
                                root.selectedIndex = Math.min(root.filteredEmojis.length - 1, root.selectedIndex + cols);
                                event.accepted = true;
                            }
                        } else if (event.key === Qt.Key_Up) {
                            if (root.filteredEmojis.length > 0) {
                                root.selectedIndex = Math.max(0, root.selectedIndex - cols);
                                event.accepted = true;
                            }
                        } else if (event.key === Qt.Key_Right) {
                            if (root.filteredEmojis.length > 0) {
                                root.selectedIndex = Math.min(root.filteredEmojis.length - 1, root.selectedIndex + 1);
                                event.accepted = true;
                            }
                        } else if (event.key === Qt.Key_Left) {
                            if (root.filteredEmojis.length > 0) {
                                root.selectedIndex = Math.max(0, root.selectedIndex - 1);
                                event.accepted = true;
                            }
                        } else if (event.key === Qt.Key_Return || event.key === Qt.Key_Enter) {
                            if (root.filteredEmojis.length > 0 && root.selectedIndex >= 0 && root.selectedIndex < root.filteredEmojis.length) {
                                root.copyEmoji(root.filteredEmojis[root.selectedIndex].emoji);
                                event.accepted = true;
                            }
                        } else if (event.key === Qt.Key_Escape) {
                            root.closeRequested();
                            event.accepted = true;
                        }
                    }
                }

                // Clear button
                Text {
                    id: clearButton
                    text: ""
                    font.family: root.iconFontFamily
                    font.pixelSize: 14
                    color: clearMouseArea.containsMouse ? "#ffffff" : Qt.rgba(1, 1, 1, 0.35)
                    visible: root.searchText !== ""
                    anchors.verticalCenter: parent.verticalCenter

                    MouseArea {
                        id: clearMouseArea
                        anchors.fill: parent
                        hoverEnabled: true
                        onClicked: {
                            searchInput.text = "";
                            searchInput.forceActiveFocus();
                        }
                    }
                }
            }
        }

        // Horizontal Category Bar (Premium Segment Control Style)
        Rectangle {
            id: categoryBar
            width: parent.width
            height: 38
            radius: 12
            color: Qt.rgba(1, 1, 1, 0.03)
            visible: root.searchText === ""

            Row {
                anchors.centerIn: parent
                spacing: 8

                Repeater {
                    model: EmojiData.CATEGORIES

                    delegate: Item {
                        required property var modelData
                        required property int index

                        width: 44
                        height: 30

                        readonly property bool isSelected: index === root.selectedCategoryIndex

                        Rectangle {
                            anchors.fill: parent
                            radius: 8
                            color: isSelected 
                                ? Qt.rgba(1, 1, 1, 0.08) 
                                : (catMouseArea.containsMouse ? Qt.rgba(1, 1, 1, 0.03) : "transparent")

                            Behavior on color {
                                ColorAnimation { duration: 120 }
                            }

                            Text {
                                text: modelData.icon
                                font.pixelSize: 16
                                anchors.centerIn: parent
                                scale: isSelected ? 1.15 : 1.0
                                opacity: isSelected ? 1.0 : 0.65

                                Behavior on scale {
                                    NumberAnimation { duration: 120; easing.type: Easing.OutCubic }
                                }
                                Behavior on opacity {
                                    NumberAnimation { duration: 120 }
                                }
                            }
                        }

                        MouseArea {
                            id: catMouseArea
                            anchors.fill: parent
                            hoverEnabled: true
                            onClicked: {
                                root.selectedCategoryIndex = index;
                                searchInput.forceActiveFocus();
                            }
                        }
                    }
                }
            }
        }

        // Category / Search Label (Sleek text label)
        Text {
            width: parent.width
            height: 18
            text: root.searchText !== "" 
                ? qsTr("Search Results") 
                : EmojiData.CATEGORIES[root.selectedCategoryIndex].name
            font.family: root.textFontFamily
            font.pixelSize: 11
            font.weight: Font.DemiBold
            color: Qt.rgba(1, 1, 1, 0.35)
        }

        // Flickable Area for Grid (Scrollbars Hidden)
        Flickable {
            id: flickable
            width: parent.width
            height: parent.height - searchBarContainer.height - (categoryBar.visible ? categoryBar.height : 0) - 46
            contentWidth: width
            contentHeight: grid.height
            clip: true
            boundsBehavior: Flickable.StopAtBounds

            // Grid View of Emojis
            Grid {
                id: grid
                width: parent.width
                columns: root.columns
                spacing: 10

                Repeater {
                    model: root.filteredEmojis

                    delegate: Item {
                        id: emojiItem
                        required property var modelData
                        required property int index

                        width: root.itemWidth
                        height: root.itemHeight

                        readonly property bool isSelected: index === root.selectedIndex

                        Rectangle {
                            anchors.fill: parent
                            radius: 10
                            color: isSelected 
                                ? Qt.rgba(1, 1, 1, 0.08) 
                                : (emojiMouseArea.containsMouse ? Qt.rgba(1, 1, 1, 0.03) : "transparent")
                            border.width: 0
                            
                            scale: isSelected ? 1.1 : 1.0
                            
                            Behavior on color { ColorAnimation { duration: 120; easing.type: Easing.OutQuad } }
                            Behavior on scale { NumberAnimation { duration: 120; easing.type: Easing.OutCubic } }

                            Text {
                                text: modelData.emoji
                                font.pixelSize: 22
                                anchors.centerIn: parent
                            }
                        }

                        MouseArea {
                            id: emojiMouseArea
                            anchors.fill: parent
                            hoverEnabled: true
                            onContainsMouseChanged: {
                                if (containsMouse) {
                                    root.selectedIndex = index;
                                }
                            }
                            onClicked: {
                                root.copyEmoji(modelData.emoji);
                            }
                        }
                    }
                }
            }
        }
    }

    // No emojis found indicator
    Column {
        anchors.centerIn: parent
        anchors.verticalCenterOffset: 30
        visible: root.filteredEmojis.length === 0
        spacing: 12

        Text {
            text: "🔍"
            font.pixelSize: 32
            opacity: 0.2
            anchors.horizontalCenter: parent.horizontalCenter
        }

        Text {
            text: qsTr("No matching emojis found")
            font.family: root.textFontFamily
            font.pixelSize: 13
            color: Qt.rgba(1, 1, 1, 0.2)
            anchors.horizontalCenter: parent.horizontalCenter
        }
    }
}
