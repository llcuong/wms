import { View, Text, ScrollView, TouchableOpacity, SafeAreaView, Modal, FlatList } from 'react-native';
import { ChevronDown, Warehouse, Search, Bell, Check, X } from 'lucide-react-native';
import { useState } from 'react';

const WAREHOUSES = [
    { id: '1', name: 'Kho Đóng Gói', address: 'Giang Điền' },
    { id: '2', name: 'Kho Khuôn', address: 'Giang Điền' },
    { id: '3', name: 'Kho Bán Thành Phẩm', address: 'Giang Điền' },
    { id: '4', name: 'Kho Thành Phẩm', address: 'Giang Điền' },
];

export default function HomeScreen() {
    const [selectedWarehouse, setSelectedWarehouse] = useState(WAREHOUSES[0]);
    const [modalVisible, setModalVisible] = useState(false);

    const renderWarehouseItem = ({item}: { item: typeof WAREHOUSES[0] }) => (
        <TouchableOpacity
            className={`flex-row items-center p-4 mb-3 rounded-2xl border ${selectedWarehouse.id === item.id ? 'bg-green-50 border-green-500' : 'bg-neutral-50 border-neutral-200'}`}
            onPress={() => {
                setSelectedWarehouse(item);
                setModalVisible(false);
            }}>
            <View className={`w-10 h-10 rounded-full items-center justify-center mr-3 ${selectedWarehouse.id === item.id ? 'bg-green-100' : 'bg-white'}`}>
                <Warehouse size={20} color={selectedWarehouse.id === item.id ? '#16a34a' : '#737373'}/>
            </View>
            <View className="flex-1">
                <Text className={`font-bold text-base ${selectedWarehouse.id === item.id ? 'text-green-700' : 'text-neutral-800'}`}>
                    {item.name}
                </Text>
                <Text className="text-neutral-500 text-sm">{item.address}</Text>
            </View>
            {selectedWarehouse.id === item.id && (
                <Check size={20} color="#16a34a"/>
            )}
        </TouchableOpacity>
    );

    return (
        <SafeAreaView className="flex-1 bg-white">

            <View className="px-4 py-2 flex-row items-center justify-between border-b border-neutral-100 pb-4 w-full">
                <View>
                    <TouchableOpacity
                        className="flex-row items-center"
                        onPress={() => setModalVisible(true)}
                    >
                        <Text className="text-xl font-bold text-neutral-900 mr-1">
                            {selectedWarehouse.name.split(' - ')[0]}
                        </Text>
                        <ChevronDown size={20} color="#16a34a"/>
                    </TouchableOpacity>
                </View>

                <View className="flex-row gap-3">
                    <TouchableOpacity
                        className="w-10 h-10 bg-neutral-50 rounded-full items-center justify-center border border-neutral-100">
                        <Bell size={20} color="black"/>
                        <View className="absolute top-2 right-2.5 w-2 h-2 bg-red-500 rounded-full"/>
                    </TouchableOpacity>
                </View>
            </View>

            <ScrollView className="flex-1 px-4 pt-4" showsVerticalScrollIndicator={false}>

                <View className="flex-row justify-between mb-6 w-full">

                </View>

            </ScrollView>

            <Modal
                animationType="slide"
                transparent={true}
                visible={modalVisible}
                onRequestClose={() => setModalVisible(false)}
            >
                <View className="flex-1 justify-end bg-black/40">
                    <View className="bg-white rounded-t-3xl p-5 h-[50%] shadow-2xl">

                        <View className="flex-row justify-between items-center mb-4">
                            <Text className="text-lg font-bold text-neutral-900">Chọn kho làm việc</Text>
                            <TouchableOpacity onPress={() => setModalVisible(false)}
                                              className="bg-neutral-100 p-2 rounded-full">
                                <X size={20} color="black"/>
                            </TouchableOpacity>
                        </View>

                        <View className="h-[1px] bg-neutral-100 mb-4 w-full"/>

                        <FlatList
                            data={WAREHOUSES}
                            keyExtractor={(item) => item.id}
                            renderItem={renderWarehouseItem}
                            showsVerticalScrollIndicator={false}
                        />
                    </View>
                </View>
            </Modal>

        </SafeAreaView>
    );
}