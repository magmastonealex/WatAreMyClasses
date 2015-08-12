//
//  ClassesViewController.m
//  WatAreMyClasses
//
//  Created by Alex Roth on 2015-08-11.
//  Copyright © 2015 Alex Roth. All rights reserved.
//

#import "ClassesViewController.h"
#import "WatClass.h"
#import "DataCacher.h"
@interface ClassesViewController ()
@property (nonatomic) NSArray * classesArray;

@end

@implementation ClassesViewController
@synthesize classesArray,doneGoto;

- (void)viewDidLoad {
    [super viewDidLoad];
    DataCacher * sCache=[DataCacher sharedCache];
    classesArray=sCache.classes;
    doneGoto=@"none";

    // Do any additional setup after loading the view.
}
-(void)viewDidAppear:(BOOL)animated{
    [super viewDidAppear:animated];
    if (classesArray==nil){
        [self performSegueWithIdentifier:@"ClassesLeave" sender:self];
    }
}

- (void)didReceiveMemoryWarning {
    [super didReceiveMemoryWarning];
    // Dispose of any resources that can be recreated.
}

-(void)tableView:(UITableView *)tableView didSelectRowAtIndexPath:(NSIndexPath *)indexPath{
    NSArray * whereComponents = [((WatClass*)[classesArray objectAtIndex:indexPath.row]).where componentsSeparatedByString:@" "];
    doneGoto=[NSString stringWithFormat:@"b-%@",[whereComponents objectAtIndex:0]];
    
    [self performSegueWithIdentifier:@"ClassesLeave" sender:self];
}
- (NSInteger)tableView:(UITableView *)tableView numberOfRowsInSection:(NSInteger)section
{
    return [classesArray count];
}

- (UITableViewCell *)tableView:(UITableView *)tableView cellForRowAtIndexPath:(NSIndexPath *)indexPath
{
    static NSString *simpleTableIdentifier = @"ClassCell";
    
    UITableViewCell *cell = [tableView dequeueReusableCellWithIdentifier:simpleTableIdentifier];
    
    if (cell == nil) {
        cell = [[UITableViewCell alloc] initWithStyle:UITableViewCellStyleDefault reuseIdentifier:simpleTableIdentifier];
    }
    WatClass * cls = [classesArray objectAtIndex:indexPath.row];
    
    UILabel * firstLine = (UILabel *)[cell viewWithTag:5]; //First line
    UILabel * secondLine = (UILabel *)[cell viewWithTag:10]; //second line
    
    NSArray *timeComponents1 = [cls.timestamp componentsSeparatedByString:@" "];
    NSArray *timeComponents2 = [cls.timeend componentsSeparatedByString:@" "];
    [secondLine setText:
     [NSString stringWithFormat:@"%@ -> %@",[timeComponents1 objectAtIndex:0],[timeComponents2 objectAtIndex:0]]
     ];
    
    NSArray * nameComponents = [cls.class_name componentsSeparatedByString:@"-"];
    [firstLine setText:
     [NSString stringWithFormat:@"%@ - %@ - %@",cls.type,[nameComponents objectAtIndex:0],cls.where]
     ];
    
    return cell;
}

/*
#pragma mark - Navigation

// In a storyboard-based application, you will often want to do a little preparation before navigation
- (void)prepareForSegue:(UIStoryboardSegue *)segue sender:(id)sender {
    // Get the new view controller using [segue destinationViewController].
    // Pass the selected object to the new view controller.
}
*/

@end
