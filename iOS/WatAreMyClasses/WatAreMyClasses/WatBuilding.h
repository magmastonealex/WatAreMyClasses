//
//  WatBuilding.h
//  WatAreMyClasses
//
//  Created by Alex Roth on 2015-08-07.
//  Copyright © 2015 Alex Roth. All rights reserved.
//

#import <Foundation/Foundation.h>
#import <Mantle/Mantle.h>
//Basic container for a Building
@interface WatBuilding : MTLModel<MTLJSONSerializing>
@property (nonatomic) NSString * name;
@property (nonatomic) NSString * bid;
@end
